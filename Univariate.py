class Univariate():
    def quanQual(dataset):
        quan=[]
        qual=[]
        for columnName in dataset.columns:
            #print(columnName)
            if(dataset[columnName].dtype=='O'):
                #print("qual")
                qual.append(columnName)
            else:
                #print("quan")
                quan.append(columnName)
        return quan,qual
        
    def Univariate(quan,dataset):
        descriptive=pd.DataFrame(index=["Mean","Median","Mode","Q1:25%","Q2:50%","Q3:75%","99%","Q4:100%",
                                    "IQR","1.5 rule","Lesser","Greater","Min","Max"],columns=quan)
        for columnName in quan:
            descriptive[columnName]["Mean"]=dataset[columnName].mean()
            descriptive[columnName]["Median"]=dataset[columnName].median()
            descriptive[columnName]["Mode"]=dataset[columnName].mode()[0]
            descriptive[columnName]["Q1:25%"]=dataset.describe()[columnName]["25%"]
            descriptive[columnName]["Q2:50%"]=dataset.describe()[columnName]["50%"]
            descriptive[columnName]["Q3:75%"]=dataset.describe()[columnName]["75%"]
            descriptive[columnName]["99%"]=np.percentile(dataset[columnName],99)
            descriptive[columnName]["Q4:100%"]=dataset.describe()[columnName]["max"]
            descriptive[columnName]["IQR"]=descriptive[columnName]["Q3:75%"]- descriptive[columnName]["Q1:25%"]
            descriptive[columnName]["1.5 rule"]=1.5*descriptive[columnName]["IQR"]
            descriptive[columnName]["Lesser"]= descriptive[columnName]["Q1:25%"] - descriptive[columnName]["1.5 rule"]
            descriptive[columnName]["Greater"]=descriptive[columnName]["Q3:75%"] + descriptive[columnName]["1.5 rule"]
            descriptive[columnName]["Min"]= dataset[columnName].min()
            descriptive[columnName]["Max"]= dataset[columnName].max()
            descriptive[columnName]["Skew"]= dataset[columnName].skew()
            descriptive[columnName]["Kurtosis"]= dataset[columnName].kurtosis()
            descriptive[columnName]["Var"]= dataset[columnName].var()
            descriptive[columnName]["Std"]= dataset[columnName].std()
        return descriptive
        
    def findoutlier(quan):
        lesser=[]
        greater=[]
        for columnName in quan:
            if(descriptive[columnName]["Min"]< descriptive[columnName]["Lesser"]):
                lesser.append(columnName)
            if(descriptive[columnName]["Max"]> descriptive[columnName]["Greater"]):
                greater.append(columnName)
        return lesser, greater

    def replaceoutlier(descriptive,dataset):
        for columnName in lesser:
            dataset[columnName][dataset[columnName]<descriptive[columnName]["Lesser"]]= descriptive[columnName]["Lesser"]
        for columnName in greater:
            dataset[columnName][dataset[columnName]>descriptive[columnName]["Greater"]]=descriptive[columnName]["Greater"]
        return descriptive

    def get_pdf_probability(dataset,startrange,endrange): 
        from matplotlib import pyplot 
        from scipy.stats import norm 
        import seaborn as sns 
        ax= sns.distplot(dataset,kde=True,kde_kws={'color':'blue'},color='Green')
        pyplot.axvline(startrange,color='Red') 
        pyplot.axvline(endrange,color='Red')
        sample= dataset  
        sample_mean= sample.mean() 
        sample_std= sample.std() 
        print('Mean=%.3f,Standard Deviation=%.3f' % (sample_mean,sample_std)) 
        dist= norm(sample_mean,sample_std) 
        values=[]
        probabilities=[]
        for value in range(startrange,endrange):
            values.append(value)
        for value in values:
            pdf_value=dist.pdf(value)
            probabilities.append(pdf_value)
        prob= sum(probabilities) 
        print("The area between range({},{}):{}".format(startrange,endrange,prob)) 
        return prob

    def StdNBgraph(dataset): # Defines the function
        import seaborn as sns # Used for histogram.
        import numpy as np # use for numpy array
        mean = dataset.mean() # Calculate the mean of dataset
        std = dataset.std() # Calculate the standard deivation of dataset.
        values =[i for i in dataset] # used one line loop to get the values as list from dataset
        z_score = [((j- mean)/std) for j in values] # Created formula to get z_score using values
        sns.distplot(z_score,kde=True) # to plot the distribution of data using z_score
        z_mean = sum(z_score)/len(z_score) # to check the mean of z_score. mean value should be 0.
        print("Mean of z_score:",round(z_mean,4))
        z_std= np.std(z_score) # to check the std of z_score. std should be 1.
        print("Standard deviation of z_score:",round(z_std,4))
        return z_mean,z_std





        