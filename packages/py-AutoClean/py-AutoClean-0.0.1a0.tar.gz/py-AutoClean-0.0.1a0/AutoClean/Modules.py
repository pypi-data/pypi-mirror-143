from timeit import default_timer as timer
import numpy as np
import pandas as pd
from math import isnan
from sklearn import preprocessing
from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from loguru import logger
import warnings
warnings.filterwarnings("ignore")

class MissingValues:

    def handle(self, df, _n_neighbors=3):
        # function for handling missing values in the data
        logger.info('Started handling of missing values...', self.missing_num.upper())
        start = timer()
        self.count_missing = df.isna().sum().sum()

        if self.count_missing != 0:
            logger.info('Found a total of {} missing value(s)', self.count_missing)
            df = df.dropna(how='all')
            df.reset_index(drop=True)
            
            if self.missing_num:
                logger.info('Started handling of NUMERICAL missing values... Method: "{}"', self.missing_num.upper())
                # automated handling of missing values
                if self.missing_num == 'auto':
                    self.missing_num = 'linreg'
                    lr = LinearRegression()
                    df = MissingValues._lin_regression_impute(self, df, lr)
                    self.missing_num = 'knn'
                    imputer = KNNImputer(n_neighbors=_n_neighbors)
                    df = MissingValues._impute(self, df, imputer, type='num')
                # linear regression imputation
                elif self.missing_num == 'linreg':
                    lr = LinearRegression()
                    df = MissingValues._lin_regression_impute(self, df, lr)
                # knn imputation (default)
                elif self.missing_num == 'knn':
                    imputer = KNNImputer(n_neighbors=_n_neighbors)
                    df = MissingValues._impute(self, df, imputer, type='num')
                # mean, median or mode imputation
                elif self.missing_num in ['mean', 'median', 'most_frequent']:
                    imputer = SimpleImputer(strategy=self.missing_num)
                    df = MissingValues._impute_missing(self, df, imputer, type='num')
                # delete missing values
                elif self.missing_num == 'delete':
                    df = MissingValues._delete(self, df, type='num')
                    logger.debug('Deletion of {} NUMERIC missing value(s) succeeded', self.count_missing-df.isna().sum().sum())      

            if self.missing_categ:
                logger.info('Started handling of CATEGORICAL missing values... Method: "{}"', self.missing_categ.upper())
                # automated handling of missing values
                if self.missing_categ == 'auto':
                    self.missing_categ = 'logreg'
                    lr = LogisticRegression()
                    df = MissingValues._log_regression_impute(self, df, lr)
                    self.missing_categ = 'knn'
                    imputer = KNNImputer(n_neighbors=_n_neighbors)
                    df = MissingValues._impute(self, df, imputer, type='categ')
                elif self.missing_categ == 'logreg':
                    lr = LogisticRegression()
                    df = MissingValues._log_regression_impute(self, df, lr)
                # knn imputation (default)
                elif self.missing_categ == 'knn':
                    imputer = KNNImputer(n_neighbors=_n_neighbors)
                    df = MissingValues._impute(self, df, imputer, type='categ')  
                # mode imputation
                elif self.missing_categ == 'most_frequent':
                    imputer = SimpleImputer(strategy=self.missing_categ)
                    df = MissingValues._impute(self, df, imputer, type='categ')
                # delete missing values                    
                elif self.missing_categ == 'delete':
                    df = MissingValues._delete(self, df, type='categ')
                    logger.debug('Deletion of {} CATEGORICAL missing value(s) succeeded', self.count_missing-df.isna().sum().sum())
        else:
            logger.debug('{} missing values found', self.count_missing)
        end = timer()
        logger.info('Completed handling of missing values in {} seconds', round(end-start, 6))
        return df

    def _impute(self, df, imputer, type):
        cols_num = df.select_dtypes(include=np.number).columns 
        if type == 'num':
            # numerical features
            for feature in df.columns: 
                if feature in cols_num:
                    if df[feature].isna().sum().sum() != 0:
                        try:
                            df_imputed = pd.DataFrame(imputer.fit_transform(np.array(df[feature]).reshape(-1, 1)), columns=[feature])
                            counter = sum(1 for i, j in zip(list(df_imputed[feature]), list(df[feature])) if i != j)
                            if (df[feature].fillna(-9999) % 1  == 0).all():
                                # round back to INTs, if original data were INTs
                                df[feature] = df_imputed
                                df[feature] = df[feature].astype(int)                                        
                            else:
                                df[feature] = df_imputed
                            if counter != 0:
                                logger.debug('{} imputation of {} value(s) succeeded for feature "{}"', self.missing_num.upper(), counter, feature)
                        except:
                            logger.warning('{} imputation failed for feature "{}"', self.missing_num.upper(), feature)
        else:
            # categorical features
            for feature in df.columns:
                if feature not in cols_num:
                    #if feature == 'datetime':
                        # here it finds 6 whereas there are only 4
                    if df[feature].isna().sum()!= 0:
                        try:
                            mapping = dict()
                            mappings = {k: i for i, k in enumerate(df[feature].dropna().unique(), 0)}
                            mapping[feature] = mappings
                            df[feature] = df[feature].map(mapping[feature])

                            df_imputed = pd.DataFrame(imputer.fit_transform(np.array(df[feature]).reshape(-1, 1)), columns=[feature])    
                            counter = sum(1 for i, j in zip(list(df_imputed[feature]), list(df[feature])) if i != j)

                            df[feature] = df_imputed
                            df[feature] = df[feature].astype(int)  

                            mappings_inv = {v: k for k, v in mapping[feature].items()}
                            df[feature] = df[feature].map(mappings_inv)
                            if counter != 0:
                                logger.debug('{} imputation of {} value(s) succeeded for feature "{}"', self.missing_categ.upper(), counter, feature)
                        except:
                            logger.warning('{} imputation failed for feature "{}"', self.missing_categ.upper(), feature)
        return df

    def _lin_regression_impute(self, df, model):
        cols_num = df.select_dtypes(include=np.number).columns
        mapping = dict()
        for feature in df.columns:
            if feature not in cols_num:
                mappings = {k: i for i, k in enumerate(df[feature].dropna().unique(), 0)}
                mapping[feature] = mappings
                df[feature] = df[feature].map(mapping[feature])
            
        for feature in cols_num: 
                try:
                    test_df = df[df[feature].isnull()==True].dropna(subset=[x for x in df.columns if x != feature])
                    train_df = df[df[feature].isnull()==False].dropna(subset=[x for x in df.columns if x != feature])
                    
                    #print(train_df.isna().sum().sum())
                    #print(np.all(np.isfinite(train_df)))

                    pipe = make_pipeline(StandardScaler(), model)
                    
                    if len(test_df.index) != 0:

                        y = np.log(train_df[feature]) #np.log
                        #print("Y shape", y.shape)
                        #print(y.isna().sum().sum())
                        #print(np.all(np.isfinite(y)))   
                        #print(y)

                        X_train = train_df.drop(feature, axis=1)
                        test_df.drop(feature, axis=1, inplace=True)
                        
                        try:
                            model = pipe.fit(X_train, y)
                        except:
                            y = train_df[feature]
                            model = pipe.fit(X_train, y)

                        #print(cross_val_score(model, X_train, y, scoring='neg_root_mean_squared_error', cv=5)) #cross val
                        #cv = KFold(n_splits=5, random_state=1, shuffle=True)
                        #print((KFold(n_splits=5, random_state=1, shuffle=True)))
                        #print(model.score(X_train, y))
                        
                        if (y == train_df[feature]).all():
                            pred = model.predict(test_df) # predicted values np.exp()
                        else:
                            pred = np.exp(model.predict(test_df))
                        test_df[feature]= pred

                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            # round back to INTs, if original data were INTs
                            test_df[feature] = test_df[feature].round()
                            test_df[feature] = test_df[feature].astype(int)
                            df[feature].update(test_df[feature])                              
                        else:
                            df[feature].update(test_df[feature])  
                        logger.debug('LINREG imputation of {} value(s) succeeded for feature "{}"', len(pred), feature)

                except Exception as e:
                    logger.warning('LINREG imputation failed for feature "{}"', feature)

                    print(feature, e)
                    print(train_df)

        for feature in df.columns: 
            try:   
                mappings_inv = {v: k for k, v in mapping[feature].items()}
                df[feature] = df[feature].map(mappings_inv)
            except Exception as e:
                pass

        return df

    def _log_regression_impute(self, df, model):
        cols_num = df.select_dtypes(include=np.number).columns
        mapping = dict()
        for feature in df.columns:
            if feature not in cols_num:
                mappings = {k: i for i, k in enumerate(df[feature].dropna().unique(), 0)}
                mapping[feature] = mappings
                df[feature] = df[feature].map(mapping[feature])
        
        target_cols = [x for x in df.columns if x not in cols_num]
            
        for feature in df.columns: 
            if feature in target_cols:
                try:
                    test_df = df[df[feature].isnull()==True].dropna(subset=[x for x in df.columns if x != feature])
                    train_df = df[df[feature].isnull()==False].dropna(subset=[x for x in df.columns if x != feature])
                    if len(test_df.index) != 0:

                        pipe = make_pipeline(StandardScaler(), model)

                        y = train_df[feature]
                        train_df.drop(feature, axis=1, inplace=True)
                        test_df.drop(feature, axis=1, inplace=True)

                        # use response int and regressors to predict y
                        model = pipe.fit(train_df, y)
                        
                        pred = model.predict(test_df) # predicted values
                        test_df[feature]= pred

                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            # round back to INTs, if original data were INTs
                            test_df[feature] = test_df[feature].round()
                            test_df[feature] = test_df[feature].astype(int)
                            df[feature].update(test_df[feature])                              

                        logger.debug('LOGREG imputation of {} value(s) succeeded for feature "{}"', len(pred), feature)

                except:
                    logger.warning('LOGREG imputation failed for feature "{}"', feature)

        for feature in df.columns: 
            try:   
                mappings_inv = {v: k for k, v in mapping[feature].items()}
                df[feature] = df[feature].map(mappings_inv)
            except Exception as e:
                pass     

        return df

    def _delete(self, df, type):
        cols_num = df.select_dtypes(include=np.number).columns 
        if type == 'num':
            # numerical features
            for feature in df.columns: 
                if feature in cols_num:
                    df = df.dropna(subset=[feature])
                    df.reset_index(drop=True)
        else:
            # categorical features
            for feature in df.columns:
                if feature not in cols_num:
                    df = df.dropna(subset=[feature])
                    df.reset_index(drop=True)
        return df                    

class Outliers:

    def handle(self, df):
        #defines observations as outliers if they are outside of range [Q1-1.5*IQR ; Q3+1.5*IQR] whereas IQR is the interquartile range.
        if self.outliers:
            logger.info('Started handling of outliers... Method: "{}"', self.outliers.upper())
            start = timer()   

            if self.outliers == 'winz':  
                df = Outliers._winsorization(self, df)

            elif self.ourliers == 'delete':
                df = Outliers._delete(self, df)
            
            end = timer()
            logger.info('Completed handling of outliers in {} seconds', round(end-start, 6))
        return df     

    def _winsorization(self, df):
        cols_num = df.select_dtypes(include=np.number).columns    
        for feature in cols_num:           
            counter = 0
            # compute outlier bounds
            lower_bound, upper_bound = Outliers._compute_bounds(self, df, feature)    
            for row_index, row_val in enumerate(df[feature]):
                if row_val < lower_bound or row_val > upper_bound:
                    if row_val < lower_bound:
                        if (df[feature].fillna(-9999) % 1  == 0).all():
                                df.loc[row_index, feature] = lower_bound
                                df[feature] = df[feature].astype(int) 
                        else:    
                            df.loc[row_index, feature] = lower_bound
                        counter += 1
                    else:
                        if (df[feature].fillna(-9999) % 1  == 0).all():
                            df.loc[row_index, feature] = upper_bound
                            df[feature] = df[feature].astype(int) 
                        else:
                            df.loc[row_index, feature] = upper_bound
                        counter += 1
            if counter != 0:
                logger.debug('Outlier imputation of {} value(s) succeeded for feature "{}"', counter, feature)        
        return df

    def _delete(self, df):
        cols_num = df.select_dtypes(include=np.number).columns    
        for feature in cols_num:
            counter = 0
            lower_bound, upper_bound = Outliers._compute_bounds(self, df, feature)    
            # delete observations containing outliers            
            for row_index, row_val in enumerate(df[feature]):
                if row_val < lower_bound or row_val > upper_bound:
                    df = df.drop(row_index)
                    counter +=1
            df = df.reset_index(drop=True)
            if counter != 0:
                logger.debug('Deletion of {} outliers succeeded for feature "{}"', counter, feature)
        return df

    def _compute_bounds(self, df, col):
        colSorted = sorted(df[col])
        
        q1, q3 = np.percentile(colSorted, [25, 75])
        iqr = q3 - q1

        lb = q1 - (self.outlier_param * iqr) 
        ub = q3 + (self.outlier_param * iqr) 

        return lb, ub    

class Adjust:

    def convert_datetime(self, df):
        if self.extract_datetime:
            logger.info('Started conversion of DATETIME features... Granularity: {}', self.extract_datetime)
            start = timer()
            cols = set(df.columns) ^ set(df.select_dtypes(include=np.number).columns) 

            for feature in cols: 
                try:
                    # convert features encoded as strings to type datetime ['D','M','Y','h','m','s']
                    df[feature] = pd.to_datetime(df[feature], infer_datetime_format=True)
                    try:
                        df['Day'] = pd.to_datetime(df[feature]).dt.day

                        if self.extract_datetime in ['M','Y','h','m','s']:
                            df['Month'] = pd.to_datetime(df[feature]).dt.month

                            if self.extract_datetime in ['Y','h','m','s']:
                                df['Year'] = pd.to_datetime(df[feature]).dt.year

                                if self.extract_datetime in ['h','m','s']:
                                    df['Hour'] = pd.to_datetime(df[feature]).dt.hour

                                    if self.extract_datetime in ['m','s']:
                                        df['Minute'] = pd.to_datetime(df[feature]).dt.minute

                                        if self.extract_datetime in ['s']:
                                            df['Sec'] = pd.to_datetime(df[feature]).dt.second
                        
                        logger.debug('Conversion to DATETIME succeeded for feature "{}"', feature)

                        try: 
                            # check if entries for the extracted dates/times are valid, otherwise drop
                            if (df['Hour'] == 0).all() and (df['Minute'] == 0).all() and (df['Sec'] == 0).all():
                                df.drop('Hour', inplace = True, axis =1 )
                                df.drop('Minute', inplace = True, axis =1 )
                                df.drop('Sec', inplace = True, axis =1 )
                            elif (df['Day'] == 0).all() and (df['Month'] == 0).all() and (df['Year'] == 0).all():
                                df.drop('Day', inplace = True, axis =1 )
                                df.drop('Month', inplace = True, axis =1 )
                                df.drop('Year', inplace = True, axis =1 )   
                        except:
                            pass          
                    
                    except:
                        # feature cannot be converted to datetime
                        logger.warning('Conversion to DATETIME failed for "{}"', feature)
                except:
                    pass

            end = timer()
            logger.info('Completed conversion of DATETIME features in {} seconds', round(end-start, 4))
        return df

    def round_values(self, df, input_data):
        # function that checks datatypes of features and converts them if necessary
        logger.info('Started feature type conversion...')
        start = timer()
        counter = 0
        cols_num = df.select_dtypes(include=np.number).columns
        for feature in cols_num:

                # check if all values are integers
                if (df[feature].fillna(-9999) % 1  == 0).all():
                    try:
                        # encode FLOATs with only 0 as decimals to INT
                        df[feature] = df[feature].astype(int)
                        counter += 1
                        logger.debug('Conversion to type INT succeeded for feature "{}"', feature)
                    except:
                        logger.warning('Conversion to type INT failed for feature "{}"', feature)
                else:
                    try:
                        # round the number of decimals of FLOATs back to original
                        dec = None
                        for value in input_data[feature]:
                            try:
                                if dec == None:
                                    dec = str(value)[::-1].find('.')
                                else:
                                    if str(value)[::-1].find('.') > dec:
                                        dec = str(value)[::-1].find('.')
                            except:
                                pass
                        df[feature] = df[feature].round(decimals = dec)
                        counter += 1
                        logger.debug('Conversion to type FLOAT succeeded for feature "{}"', feature)
                    except:
                        logger.warning('Conversion to type FLOAT failed for feature "{}"', feature)
        end = timer()
        logger.info('Completed feature type conversion for {} feature(s) in {} seconds', counter, round(end-start, 6))
        return df

class EncodeCateg:

    def handle(self, df):
        if self.encode_categ[0]:
            # select non numeric features
            cols_categ = set(df.columns) ^ set(df.select_dtypes(include=np.number).columns) 
            # check if all columns should be encoded
            if len(self.encode_categ) == 1:
                target_cols = cols_categ
            else:
                target_cols = self.encode_categ[1]
            logger.info('Started encoding categorical features... Method: "AUTO"')
            start = timer()
            for feature in target_cols:
                if feature in cols_categ:
                    # columns are column names
                    feature = feature
                else:
                    # columns are indexes
                    feature = df.columns[feature]
                    print(feature)
                try:
                    # skip encoding of datetime features
                    pd.to_datetime(df[feature])
                    logger.debug('Skipped encoding for DATETIME feature "{}"', feature)
                except:
                    try:
                        if self.encode_categ[0] == 'auto':
                            # ONEHOT encode if not more than 10 unique values to encode
                            if df[feature].nunique() <=10:
                                df = EncodeCateg._to_onehot(self, df, feature)
                                logger.debug('Encoding to ONEHOT succeeded for feature "{}"', feature)
                            # LABEL encode if not more than 20 unique values to encode
                            elif df[feature].nunique() <=20:
                                df = EncodeCateg._to_label(self, df, feature)
                                logger.debug('Encoding to LABEL succeeded for feature "{}"', feature)
                            # skip encoding if more than 20 unique values to encode
                            else:
                                logger.debug('Encoding skipped for feature "{}"', feature)   

                        elif self.encode_categ[0] == 'onehot':
                            df = EncodeCateg._to_onehot(df, feature)
                            logger.debug('Encoding to {} succeeded for feature "{}"', self.encode_categ[0].upper(), feature)
                        elif self.encode_categ[0] == 'label':
                            df = EncodeCateg._to_label(df, feature)
                            logger.debug('Encoding to {} succeeded for feature "{}"', self.encode_categ[0].upper(), feature)      
                    except:
                        logger.warning('Encoding to {} failed for feature "{}"', self.encode_categ[0].upper(), feature)    
            end = timer()
            logger.info('Completed encoding of categorical features in {} seconds', round(end-start, 6))
        return df

    def _to_onehot(self, df, col, limit=15):        
        one_hot = pd.get_dummies(df[col], prefix=col)
        if one_hot.shape[1] > limit:
            logger.warning('ONEHOT encoding for feature "{}" creates {} new features. Consider LABEL encoding instead.', col, one_hot.shape[1])
        # join the encoded df
        df = df.join(one_hot)
        return df

    def _to_label(self, df, col):
        le = preprocessing.LabelEncoder()
        
        df[col + '_lab'] = le.fit_transform(df[col].values)
        mapping = dict(zip(le.classes_, range(len(le.classes_))))
        
        for key in mapping:
            try:
                if isnan(key):               
                    replace = {mapping[key] : key }
                    df[col].replace(replace, inplace=True)
            except:
                pass
        return df