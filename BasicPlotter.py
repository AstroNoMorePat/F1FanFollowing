import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.animation import FuncAnimation

font_name = 'Silom'
gscale = 1000000

Frames = 451

SocialData = pd.read_csv('F1SocialData.txt')
SocialData = SocialData.sort_values('Post-Abu Dhabi')

Races = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]
RaceIters = np.linspace(0.0, 22.0, num=Frames)
Drivers = SocialData['Driver'].values.flatten().tolist()

#Drivers = ['Lewis Hamilton','Charles Leclerc','Sebastian Vettel','Sergio Perez','Max Verstappen','Daniel Ricciardo','Pierre Gasly','Valtteri Bottas','Nicholas Latifi']

def DriverColor(Name):
    lastname = Name.split(' ')[-1]
    if lastname == 'Hamilton' or lastname == 'Russell':
        color1 = '#00A19C'
        color2 = '#80142B'
    if lastname == 'Verstappen' or lastname == 'Perez':
        color1 = '#CC1E4A'
        color2 = '#121F45'
    if lastname == 'Leclerc' or lastname == 'Sainz':
        color1 = '#FFEB00'
        color2 = '#A6051A'
    if lastname == 'Norris' or lastname == 'Ricciardo':
        color1 = '#47C7FC'
        color2 = '#FF8000'
    if lastname == 'Stroll' or lastname == 'Vettel':
        color1 = '#CEDC00'
        color2 = '#00352F'
    if lastname == 'Ocon' or lastname == 'Alonso':
        color1 = '#FD4BC7'
        color2 = '#005BA9'
    if lastname == 'Tsunoda' or lastname == 'Gasly':
        color1 = '#F1F3F4'
        color2 = '#00293F'
    if lastname == 'Schumacher' or lastname == 'Magnussen':
        color1 = '#F9F2F2'
        color2 = '#F62039'
    if lastname == 'Bottas' or lastname == 'Guanyu':
        color1 = '#981E32'
        color2 = '#295294'
    if lastname == 'Latifi' or lastname == 'Albon':
        color1 = '#00A3E0'
        color2 = '#041E42'
    return color1, color2, lastname

def getImage(filename, zoom=0.125):
   return OffsetImage(plt.imread(filename, format="png"), zoom=zoom)

fig = plt.figure(figsize=(8,5))
plt.subplots_adjust(left=0.098, bottom=0.117, right=0.981, top=0.97, wspace=0.2, hspace=0.2)

def PlotDate(i):

    plt.clf()
    plt.figure(num=1, figsize=(8, 5))
    
    RaceVal = RaceIters[i]
    print(str(round(100.0*(RaceVal)/(RaceIters[-1]),1))+'% Complete')

    for driver_name in Drivers:
    
        #plt.figure(fig.number)
    
        PlotInt = int(RaceVal)
        
        follower_gain = SocialData[SocialData.Driver==driver_name].values.flatten().tolist()[1:]
        follower_gain = [0] + follower_gain
        follower_gain = np.array(follower_gain)/gscale
        
        primarycolor,secondarycolor,lastname = DriverColor(driver_name)
        
        #if RaceVal == 0:
        #    RacesPlot = [0]
        #    follower_gain = [0]
        if not RaceVal == PlotInt:
            if PlotInt == 0:
                last_gain = 0
            else:
                last_gain = follower_gain[PlotInt]
            next_gain = follower_gain[PlotInt+1]
            
            race_frac = RaceVal - float(PlotInt)
            
            step_gain = race_frac*(next_gain-last_gain) + last_gain
            
            RacesPlot = list(Races[0:PlotInt+1])
            follower_gain = list(follower_gain[0:PlotInt+1])
            
            RacesPlot.append(RaceVal)
            follower_gain.append(step_gain)
        else:
            RacesPlot = list(Races[0:PlotInt+1])
            follower_gain = list(follower_gain[0:PlotInt+1])
                
        plt.plot(RacesPlot, follower_gain, color=secondarycolor, linewidth=4, zorder=1)
        plt.plot(RacesPlot, follower_gain, label=driver_name, color=primarycolor, linewidth=1, zorder=2)
        plt.scatter(RacesPlot, follower_gain, color=secondarycolor, s=45, zorder=3)
        plt.scatter(RacesPlot, follower_gain, color=primarycolor, s=10, zorder=4)

        ab = AnnotationBbox(getImage('Images/'+lastname+'.png'), (RacesPlot[-1], follower_gain[-1]), frameon=False, box_alignment=(0.5,0.25))
        ab.set_zorder(5)
        plt.gca().add_artist(ab)
        
        follower_str = str(round(follower_gain[-1],2))
        if len(follower_str) < 4:
            follower_str += '0'
        plt.text(RacesPlot[-1]+0.55, follower_gain[-1], follower_str, font=font_name, fontsize=10)

    ab = AnnotationBbox(getImage('Images/F1Logo.png',0.02), (-0.25,3.625), frameon=False, box_alignment=(0.0,0.5))
    plt.gca().add_artist(ab)
    plt.text(3.425,3.565,'Social Media 2022',font=font_name,fontsize=12)

    plt.xlim(-0.5,23.75)
    plt.ylim(-0.05,3.80)
    #plt.legend(loc='best')

    plt.xlabel('Race Number',font=font_name, fontsize=12)
    plt.ylabel('Millions of Followers Gained', font=font_name, fontsize=12)

    plt.xticks(Races,font=font_name)
    plt.yticks(font=font_name)

    #plt.tight_layout()
    plt.subplots_adjust(left=0.098, bottom=0.117, right=0.981, top=0.97, wspace=0.2, hspace=0.2)
    
    #plt.show()


#for i in range(len(RaceIters)):
#    PlotDate(i)
#PlotDate(Frames-1)

ani = FuncAnimation(fig=fig, func=PlotDate, frames=Frames, interval=30, blit=False, cache_frame_data=False)
ani.save('full.gif', dpi=150)
