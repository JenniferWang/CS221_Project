# README
# So you can skip the helper function section and go to "START HERE"
# This script should be placed in the same directory as the file yelp_academic_dataset_"something".json (for example yelp_academic_dataset_business.json)

# Packages need for this script
# 1 Textblob
# To download Textblob do 
#       $ pip install -U textblob
#       $ python -m textblob.download_corpora
import os
import json
import random
import math
from textblob import TextBlob
################################### Helper Functions :: you can skip this part###################################
# select only qualify business and write their id in good_restaurants.json return a list of business_id of these resturants
def readBusinessFile(minReviews, minStars=3, maxStars=4):
    # get only business that is a resturant and has more than minReviews reviews
    businessFileName = 'yelp_academic_dataset_business.json'
    businessFilePath = businessFileName
    business_list = []
    count = 0
    with open(businessFilePath) as f:
        for line in f:
            while True:
                try:       
                    json_data = json.loads(line) 
                    if (json_data['review_count'] >=minReviews and 'Restaurants' in json_data['categories'] and json_data['stars']>=maxStars and json_data['stars']>=maxStars ):
                        business_list.append(json_data['business_id'])
                    break
                except ValueError:
                        line += next(f)
    with open('processedData/good_restaurants.json', 'w') as outfile:
        json.dump(business_list, outfile)
    return business_list 

# read good_restaurants.json
def readGoodResturantsFile():
    fileName = 'processedData/good_restaurants.json'
    filePath = fileName
    business_list = []
    with open(filePath) as f:
        for line in f:
            while True:
                try:       
                    json_data = json.loads(line) 
                    business_list.append(json_data)
                    break
                except ValueError:
                        line += next(f)
    return business_list[0]

# given business_id write a JSON file which has all reviews for that business_id
def createReviewJSONFile(business_id):
    # if the file exists , ksip
    fname = 'processedData/'+str(business_id) +'.json'
    if os.path.isfile(fname):
        print "there is a file  "+ fname
        return
    fileName = 'yelp_academic_dataset_review.json'
    filePath = fileName
    review_list=[]
    with open(filePath) as f:
        for line in f:
            while True:
                try:
                    json_data = json.loads(line) 
                    if json_data['business_id'] == business_id:
                        review_list.append(json_data)
                    break
                except ValueError:
                    line += next(f)
    # prepare to write af ile by removing teh old file if exists             
    outFileName = 'processedData/'+str(business_id) +'.json'
    try:
        os.remove(outFileName)
    except OSError:
        pass
    print outFileName
    with open(outFileName, 'w') as outfile:
        json.dump(review_list, outfile)

# gieb buysiness_id, return the list of review object for that resturant
def readReviewJSONFile(business_id):
    fileName = 'processedData/' + str(business_id) + '.json'
    review_list=[]
    with open(fileName) as f:
        for line in f:
            while True:
                try:
                    json_data = json.loads(line) 
                    review_list.append(json_data)
                    break
                except ValueError:
                    line += next(f)
    return review_list[0]
################################### End of Helper Functions ###########################################


################################### Function to map reviews to numerical rating########################
def getStars(selectedReviews):
    # input = a list consisting of reciew object
    # output = a list containing numerical rating for each review
    return [ selectedReviews[ind]['stars'] for ind in range(0, len(selectedReviews))]

def sentimentObjectivityAnalysis(selectedReviews, polarity_threshold=0, subjectivity_threshold=0.5, verbose=0):
    predicted_rating_list=[]
    for review_count in range(0, len(selectedReviews)):
        review_text = selectedReviews[review_count]['text']
        review_text_blob = TextBlob(review_text) # create TextBlob object
        if verbose == 1:
            print "==================  REVIEW NUMBER "+str(review_count)+ "================="
            print review_text
        if verbose == 2 :
            print "==================  REVIEW NUMBER "+str(review_count)+ "================="
            print "polarity / subjectivity / sentence"
        positive_count = 0
        negative_count = 0
        for sentence in review_text_blob.sentences:
            polarity_score = sentence.sentiment.polarity # ranges from -1 to 1
            subjectivity_score = sentence.sentiment.subjectivity # ranges from 0(objective) to 1(subjective)

            # polarity score
            if polarity_score > polarity_threshold:
                positive_count = positive_count+1
            elif polarity_score< polarity_threshold :  
                negative_count = negative_count+1
            # printing 
            if verbose == 2:
                print str(sentence.sentiment.polarity) + " / " + str(sentence.sentiment.subjectivity) +  " / " + str(sentence)
        if positive_count+negative_count == 0: # no useful info
            predictedRating = 2.5 # can be changed to average overall rating of yelp dataset
        else :
            predictedRating = 1 + float(positive_count)*4 / float(positive_count+negative_count)
        predicted_rating_list.append(predictedRating)

    return predicted_rating_list


################################END OF Function to map reviews to numerical rating########################

#########################################
# START HERE ###
###########################################
# remove files if exists
try:
    os.remove('good_restaurants.json')
except OSError:
    pass
try:
    os.remove('good_reviews.json')
except OSError:
    pass
directory ='processedData'
try:
    os.makedirs(directory)
except OSError as exception:
        pass

# params for the exerpiment
minReviews=400 # if a resturant has fewer than minReviews dont inlcude in the experiment
minStars=3 # if the resturant avergae star is less than minStars, dont include in the experiment
maxStars=4 # if the resturant avergae star is higher han minStars, dont include in the experiment
numTrials=100 # how many trials of sample, resample
numReviewsSelected = 5  #for each trial how many reviews are selected
numKept =50 # if there are too many resturants satisfying the condition above, keep only the first numKept resturants
verbose = 1 # set verbose to 0 so the program shuts up
# read resturant data
businessList = readBusinessFile(minReviews)
print "there are  "+ str(len(businessList)) + " satisfying the constraints of minReviews = "+str(minReviews)+"  minStars=  "+str(minStars)+"  maxStars= "+str(maxStars)
few_restaurants = businessList[0:numKept]
for business_id in few_restaurants:
   createReviewJSONFile(business_id)


# The following code perform the experiment of sampling numReviewsSelected review, get a rating from each review, 
#compute the avergae over numReviewsSelected reviews, and calculate the error. Repeat the experiment numTrials times and get the average error.
grand_err =[]
for business_id in few_restaurants: # for each business that is selected(satifying all conditions)
    review_list = readReviewJSONFile(business_id)
    all_stars =[]

    # TRUE RATING : Calculate avergae star from all available reviews
    for r in review_list:
        all_stars.append(r['stars'])
    avg_stars = sum(all_stars) / float(len(all_stars))
    print 'average stars is ' + str(avg_stars)
    numTotalReviews = len(review_list)
    # end of calulcate average stars from all reviews
    
    # perform the experiment numTrials times
    cumErr=0
    for trial in range(0, numTrials):
        samples = random.sample(range(0,numTotalReviews), numReviewsSelected)
        selectedReviews = [ review_list[ind] for ind in samples]
        # mapping function from review to numeriical rating, here we use getStar which just gets the star rating for each review and return
        #stars_list = getStars(selectedReviews)
        stars_list = sentimentObjectivityAnalysis(selectedReviews, verbose=0)
        # calculate the avergae of numberical rating
        predicted_star = sum(stars_list) / float(len(stars_list))
        cumErr = cumErr + pow((predicted_star-avg_stars),2)
    err = float(cumErr)/numTrials
    print "error is " + str(err)
    print " ======================================"
    grand_err.append(err)
print grand_err

print "***************************************"
print "***************************************"
print 'on average grand_err is  ' +str(float(sum(grand_err))/len(grand_err))

    