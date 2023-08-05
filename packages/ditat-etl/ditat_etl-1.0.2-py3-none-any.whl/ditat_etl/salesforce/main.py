import os
import json
import inspect
from datetime import timedelta, datetime
import requests
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import numpy as np
from simple_salesforce import Salesforce


from ..time import TimeIt


filedir = os.path.abspath(os.path.dirname(__file__))


class SalesforceObj():
    
    TYPES_MAPPING = {
        'string': str,
        'reference': str,
        'datetime': 'datetime',
        # 'picklist': list,
        'picklist': str,
        'boolean': bool,
        'date': 'date',
        'double': float,
        'phone': str,
        'url': str,
        'email': str,
        'id': str,
        'textarea': str,
        'int': int,
        'address': str,
        'multipicklist': list,
        'currency': int,
        'percent': float
    }

    def __init__(
        self,
        config,
        client_id=None,
        client_secret=None,
        ):
        req_params =  inspect.getargspec(Salesforce)[0]
        self.config_params = {i: j for i, j in config.items() if i in req_params}
        self.config_params['version'] = '53.0'

        self.client_id = client_id
        self.client_secret = client_secret
        self.load_client_credentials()
        
        self.access_token = None
        self.instance_url = None
        self.login()

    def load_client_credentials(self):
        if not self.client_id or not self.client_secret:

            with open(os.path.join(filedir, 'credentials.json'), 'r') as f:
                file = f.read()

            try:
                credentials = json.loads(file)
                self.client_id = credentials.get('CLIENT_ID')
                self.client_secret = credentials.get('CLIENT_SECRET')

            except Exception:
                print('Could not load SF client credentials.')

    def login(self):
        '''
        This class will eventually only use oauth2 refresh tokens because
        starting in Feb 2022, all username/password login will require MFAs

        '''
        refresh_token = self.config_params.get('session_id') 

        if refresh_token:
            print('Logging in with refresh token')
            self.refresh_token(refresh_token)
            self.sf = Salesforce(instance_url=self.instance_url, session_id=self.access_token)

        else:
            print('Logging in with username/password.')
            self.sf = Salesforce(**self.config_params)

    def refresh_token(
        self,
        refresh_token: str,
        client_id: str=None,
        client_secret: str=None,
        url="https://login.salesforce.com/services/oauth2/token",
        ):
        '''
        Refresh access token for login.

        Args:
            - refresh_token (str)

            - client_id (str, default=None)

            - client_secret (str, default=None)

            - url (str, default='https://login.salesforce.com/services/oauth2/token')
            
        '''
        payload = {
            'grant_type': 'refresh_token',
            'client_id': client_id or self.client_id,
            'client_secret': client_secret or self.client_secret,
            'refresh_token': refresh_token
        }
        resp = requests.post(url=url, data=payload).json()
        self.access_token = resp['access_token']
        self.instance_url = resp['instance_url']
            
    def check_table_exists(
        self,
        tablename,
        verbose=True
        ):
        '''
        Custom sobjects/tables are not included in the property attribute,
        hence we use this wrapper to see if the sobject exits for the client.
        
        Args:
            tablename (str): name of the sobject.

            verbose (bool, default=False): print the possible error.
        '''
        try:
            query = '''
                SELECT
                    COUNT(Id)
                FROM
                    {}
            '''.format(tablename)
            count = self.sf.query(query).get('records')[0].get('expr0')

            if count == 0:
                return None

            return True

        except Exception as e:
            if verbose:
                print(e)

            return None

    @property
    def tables(self):
        '''
        Get all the tables/SObjects
        '''
        return [obj['name'] for obj in self.sf.describe()['sobjects']]

    def get_table_info(self, tablename, columns=None):
        if not self.check_table_exists(tablename):
            return None

        table = getattr(self.sf, tablename)
        df = pd.DataFrame(table.describe()['fields'])

        if columns is not None and all(item in df['name'].tolist() for item in columns):
            df = df[columns]

        return df

    def map_types(self, df, tablename, check_column_casing=True):
        df = df.copy()
        
        info = self.get_table_info(tablename)[['name', 'type']]

        if check_column_casing:
            info['lower_name'] = info['name'].str.lower()
            case_mapping = {i: j for i, j in info.set_index('lower_name')['name'].to_dict().items() if i in df.columns} 
            df.rename(columns=case_mapping, inplace=True)

        info = info.loc[info.name.isin(df.columns)]

        info['python_type'] = info['type'].map(type(self).TYPES_MAPPING)
        info.loc[info['python_type'].isnull(), 'python_type'] = str

        mapping = info.set_index('name')['python_type'].to_dict()
        mapping = {i: j for i, j in mapping.items() if j not in [list, dict]}

        df = df[[col for col in df.columns if col in mapping.keys()]]

        for k, v in mapping.items():

            if v in [list, dict]:
                continue

            elif v == "date":
                df[k] = df[k].astype('datetime64').dt.strftime("%Y-%m-%d")

            elif v == 'datetime':
                df[k] = df[k].astype('datetime64').dt.strftime('%Y-%m-%dT00:00:00.000Z')

            else:
                df[k] = df[k].astype(v, errors='ignore')

            if v in [int, float]:
                df[k] = df[k].fillna(0, inplace=True)

        df = df.where(pd.notnull(df), None)

        return df
        
    def get_table_cols(
        self,
        tablename
        ):
        '''
        Returns all column names of table / SObject of self.sf

        Args:
            tablename (str)

        Returns
            Column names    
        '''
        return self.get_table_info(tablename, columns=['name'])['name'].tolist()

    @TimeIt()
    def query(
        self,
        tablename,
        columns=None,
        limit=None,
        df=False,
        date_from=None,
        date_to=None,
        date_window=None,
        date_window_variable='LastModifiedDate',
        verbose=False,
        timeout=None,
        max_columns=100, # SF limit on columns
        ):
        '''
        Returns dictionary of the columns requested from the table / SObject specified.
        If no columns or wrong columns are provided, it returns all the columns.

        Args:
            tablename (str): SObject Resource from self.sf
            
            columns (str: default=None): Columns names to be queried.

            limit (int): CHECK THIS! You have to add a limit.

            df(boolean default: False): Output format Dict or pd.DataFrame
            
            date_from (str, default=None): It has to be in the correct format.

            date_to (str, default=None): It has to be in the correct format.
             
            date_window (int, default=None): How many days to go back
             
            verbose (bool, default=False): print the query

        Returns:
            Output format Dict or pd.DataFrame from query

        Notes:
            - You have to decide between date_window or (date_to and date_from)
                There is no validation for this observation.

        '''
        ####
        def chunker(seq, size):
            return (seq[pos:pos + size] for pos in range(0, len(seq), size))
        #####

        if not hasattr(self.sf, tablename):
            return None

        column_names = self.get_table_cols(tablename)

        if columns is None or not all(item in column_names for item in columns):
            columns = column_names

        # Splitting in chunks
        chunks = chunker(columns, max_columns - 1)

        counter = 0
        for chunk in chunks:

            if 'Id' not in chunk:
                chunk = ['Id'] + chunk
            query_cols = ', '.join(chunk)
            query = '''
                SELECT
                    {}
                FROM
                    {}
            '''.format(
                query_cols,
                tablename
            )
            # Using date_window
            if isinstance(date_window, int) and date_window > 0:
                date_from = (
                    datetime.today() - timedelta(days=date_window)
                ).strftime('%Y-%m-%dT00:00:00.000Z')

                query += f" WHERE {date_window_variable} > {date_from}"

            # Using date_to AND date_from
            elif date_from and date_to:
                query += f" WHERE {date_window_variable} > {date_from} AND {date_window_variable} < {date_to}"

            elif date_from:
                query += f" WHERE {date_window_variable} > {date_from}"

            elif date_to:
                query += f" WHERE {date_window_variable} < {date_to}"

            if isinstance(limit, int):
                query += f' LIMIT {limit}'

            if verbose:
                print(query)

            results = self.sf.query_all(query, include_deleted=True, timeout=timeout)['records'] 

            # Only easy way to marge chunks on Id through a DataFrame
            results = pd.DataFrame.from_dict(results)

            if results.shape[0] < 1:
                return None

            if 'attributes' in results.columns:
                results.drop('attributes', axis=1, inplace=True)
            else:
                for r in results:
                    r.pop('attributes', None)

            if counter == 0:
                all_results = results
            
            else:
                all_results = pd.merge(all_results, results, on='Id', how='left')

            counter += 1            

        if df == False:
            all_results = all_results.to_dict(orient='records')

        return all_results

    ############ PARALLEL QUERY ##########
    @TimeIt()
    def query_parallel(
        self,
        tablename,
        columns=None,
        limit=None,
        df=False,
        date_window=None,
        date_window_variable='LastModifiedDate',
        verbose=False,
        n_chunks=4 # Unfortunately SF limits this to 10
    ):
        ###### 
        def limit_split(limit, n):
            if limit is None:
                return [None] * n
            l = [int(limit / n)] * n
            diff = limit % n
            for i in range(diff):
                l[i] += 1
            return l
        ############

        if date_window:
            date_from = (datetime.today() - timedelta(days=date_window))
        
        else:
            # If no date_window is provided, we retrive the oldest date according to "CreatedDate"
            date_window_variable = 'CreatedDate'

            min_date_query = f"SELECT MIN({date_window_variable}) FROM {tablename}"
            date_from_fmt = self.sf.query(min_date_query, include_deleted=True)['records'][0]['expr0']
            date_from = datetime.strptime(date_from_fmt, '%Y-%m-%dT%H:%M:%S.000+0000')

        date_from_fmt = date_from.strftime('%Y-%m-%dT00:00:00.000Z')

        date_to = datetime.today() + timedelta(days=1)

        diff = (date_to  - date_from ) / n_chunks

        chunks = []

        for i in range(n_chunks):
            start = (date_from + diff * i).strftime('%Y-%m-%dT00:00:00.000Z')
            end = (date_from + diff * (i + 1)).strftime('%Y-%m-%dT00:00:00.000Z')
            chunks.append((start, end))
        
        chunks = [c for c in chunks if c[0] != c[1]]

        payload = {
            'tablename': [tablename] * len(chunks),
            'columns': [columns] * len(chunks),
            'limit': limit_split(limit, n_chunks),
            'df': [df] * len(chunks),
            'date_from': [i[0] for i in chunks],
            'date_to': [i[1] for i in chunks],
            'data_window': [date_window_variable] * len(chunks),
            'data_window_variable': [date_window_variable] * len(chunks),
            'verbose': [verbose] * len(chunks)
        }

        with ThreadPoolExecutor() as executor:
            results = executor.map(self.query, *payload.values())
        results = [*results]
        
        if df:
            results = pd.concat(results).reset_index(drop=True)

        else:
            results = [item for sublist in results for item in sublist]
        
        return results
    ######################################

    def update(
        self,
        tablename,
        record_list,
        batch_size=10000
        ):
        '''
        Args:
            tablename (str): name of the sobject.
            record_list (list or np.array or pd.Series): List
                of records for the update
            batch_size (int, default=100000): After 10_000, it uses multithreading.

            format: "[{'Id': "11111", 'field1': '1111'}]"
        '''
        if not self.check_table_exists(tablename):
            return None

        bulk_handler = getattr(self.sf, "bulk")
        bulk_object = getattr(bulk_handler,  tablename)

        result = bulk_object.update(data=record_list, batch_size=batch_size)

        return result

    def insert_df(
        self,
        tablename: str,
        dataframe: pd.DataFrame,
        batch_size: int=10000,
        update=True,
        conflict_on='Name',
        return_response=False,
    ):
        '''
        Args:
            - tablename (str): SObject in Salesforce

            - dataframe (pd.DataFrame): Data dataframe.

            - batch_size (int, default=10_000): Salesforce default.

            - update (bool, default=True): Try updating records that have conflict on
                unique column.

            - conflict_on (str, default='Name'): Specify unique column constrain

            - return_response (bool, default=False): Include in response_payload
                the raw response from the Salesforce Api.

        Returns:
            - response_payload (dict): {"inserted": 2, 'failures': 0, "updated": 3}
                
        '''
        if not self.check_table_exists(tablename):
            return None

        df = self.map_types(df=dataframe, tablename=tablename)

        data = df.to_dict(orient='records')

        # Fix for nan
        data_list = []
        for d in data:
            new = {i: (None if j in [np.nan, 'nan'] else j) for i, j in d.items()}
            data_list.append(new)

        data = data_list

        bulk_handler = getattr(self.sf, "bulk")
        bulk_object = getattr(bulk_handler,  tablename)

        result = bulk_object.insert(data=data, batch_size=batch_size)

        insert_successes = 0
        failures = 0

        for r in result:
            if r['success'] == True:
                insert_successes += 1

            elif r['success'] == False:
                failures += 1

        response_payload = {"inserted": insert_successes, 'failures': failures}

        if return_response:
            response_payload['result'] = result

        if update:
            df['sf_status'] = [i['success'] for i in result] 

            df_to_update = df.loc[df.sf_status == False]

            if df_to_update.shape[0] > 0:

                df_to_update[conflict_on] = df_to_update[conflict_on].str.replace("'", "\\'")

                fmt_where = df_to_update[conflict_on].tolist()
                fmt_where = ','.join([f"'{i}'" for i in fmt_where])

                query = f'SELECT Id, {conflict_on} FROM {tablename} WHERE {conflict_on} IN ({fmt_where})' 

                results = self.sf.query_all(query, include_deleted=True, timeout=None)['records'] 
                results = pd.DataFrame.from_dict(results)

                if results.shape[0] > 0:

                    if 'attributes' in results.columns:
                        results.drop('attributes', axis=1, inplace=True)

                    update_mapping = results.set_index(conflict_on)['Id']

                    df_to_update['Id'] = df_to_update[conflict_on].map(update_mapping)
                    df_to_update.drop('sf_status', axis=1, inplace=True)

                    df_to_update.dropna(subset=['Id'], inplace=True)

                    update_data = df_to_update.to_dict(orient='records')
                    update_results = bulk_object.update(data=update_data, batch_size=batch_size)

                    update_successes = 0

                    for r in update_results:
                        if r['success'] == True:
                            update_successes += 1
                            response_payload['failures'] -= 1

                    response_payload['updated'] = update_successes

                    if return_response:
                        response_payload['update_result'] = update_results

            else:
                print('No records to update.')

        return response_payload 
