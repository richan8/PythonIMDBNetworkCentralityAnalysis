import urllib
import requests
import json

ApiKey='5a609835'
saveFile='db3.json'
iterationLimit=50 #Set so that if the while loop messes up then we dont send infinite requests. OMDBapi gives 1000 requests per day.

def getMovieData(name):
    url = 'http://www.omdbapi.com/?apikey='+ApiKey+'&'+'t='+name+'&type=movie'
    response = requests.get(url)
    data = json.loads(response.text)

    if(data['Response']=='True'):
        title=data['Title']
        year=data['Year']
        genre=data['Genre'].split(',')
        actors=data['Actors'].split(',')
        directors=data['Director'].split(',')
        rating=data['imdbRating']

        res={'title':title,'year':year,'genre':genre,'actors':actors,'directors':directors,'rating':rating}
        saveData(res)
        return(res)

    else:
        print(data['Error'])

def saveData(data):
    global saveFile

    with open(saveFile,'r') as f:
        x=json.loads(f.read())

    if data in x['Movies']:
        print(data['title']+' already present in local Database. Not added')
    else:
        with open(saveFile,'w') as f:
            x['Movies'].append(data)
            x=json.dumps(x)
            f.write(x)
        print('Added '+data['title'])

def getMovieList():
    with open(saveFile,'r') as f:
        x=json.loads(f.read())
        i=0
        print('----------------------------------------------------')
        for movie in x['Movies']:
            i+=1
            print('%i\t%s'%(i,movie['title']))
        print('----------------------------------------------------')

print('Input movie names to add to DB. Input 1 to See list of movies and 2 to Quit')
inp=''
i=0
while(i<iterationLimit):
    inp=input()
    i+=1
    if(inp=='1'):
        getMovieList()
    elif(inp=='2'):
        print('Bye!')
        exit()
    else:
        getMovieData(inp)

    if(i==iterationLimit):
        print('Iteration Limit Exceeded. Quitting.')
        #ITERATION LIMIT INCASE SOMETHING GOES TERRIBLY WRONG. 
        #WE DON'T WANT TO USE UP OUR 1000 API REQUESTS PER DAY