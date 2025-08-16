import exoplasim as exo   #Loads all the exoplasim commands, should always be placed at the start

model = exo.Model(workdir='loam_lgm_24',  #names the folder where files will be kept while the model runs
                  modelname='loam_lgm_24',    #sets the name for various other files and folders
                  outputtype='.nc',     #sets the filetype for the output; '.nc' is a netcdf file
                  resolution='T21',     #sets the model resolution, 'T21' is 32x64, 'T42' is 64x128, and 'T63' is 96x192
                  layers=10,            #sets the number of atmospheric layers
                  ncpus=4,              #the number of cpu cores you have
                  precision=8,          #precision of internal data; 4 is a bit faster, 8 is more stable
                  crashtolerant=True    #if the model crashes, will rewind 10 years and try again; beware of infinite loops
                 )

model.configure(timestep=45,                                #length of model timestep in minutes
                runsteps=11520,                             #the number of timesteps in the output file, usually represent 1 year
                otherargs={'NSTPW@plasim_namelist':'160'},  #how many timesteps between writes to file
                physicsfilter='gp|exp|sp',                  #can help keep model stable and reduce artifacts in tidal-locked case
                #restarfile="loam_20/MOST_REST.00060",                                #path to a restart file from a previous model; delete if not used
                flux=1367,                                  #flux of sunlight at planet in W/m^2
                startemp=5780,                              #effective temperature of star in K
                year=365.25,                                   #length of year (orbital period) in 24-hour Earth days
                eccentricity=0.016715,                      #orbital eccentricity
                fixedorbit=True,                            #prevents orbit from changing over time
                rotationperiod=1,                           #sidereal day length compared to Earth
                obliquity=23.441,                           #obliquity of planet rotation, a.k.a. axial tilt, in degrees
                lonvernaleq=102.7,                          #angle along orbit from northern fall equinox to periapsis in degrees
                synchronous=False,                          #locks the substellar point to one longitude, to simulate tidal-locking
                substellarlon=180,                          #longitude of the substellar point in degrees
                desync=0,                                   #rate of longitudinal drift of the substellar point, in degrees/minute
                tlcontrast=0,                               #initial temperature contrast between substellar and antistellar points, in K
                gravity=9.80665,                            #acceleration due to surface gravity in m/s^2
                radius=1,                                   #radius of planet relative to Earth
                landmap="SRA/hm_lgm_t21_7700_surf_0172.sra",
                topomap="SRA/hm_lgm_t21_7700_surf_0129.sra",
                pN2=0.7809,                                 #partial pressure of atmospheric nitrogen in bar
                pO2=0.2095,                                 #partial pressure of atmospheric oxygen in bar
                pAr=0.0093,                                 #partial pressure of atmospheric argon in bar
                pCO2=300e-6,                                #partial pressure of atmospheric carbon dioxide in bar
                ozone=True,                                 #presence of atmospheric ozone
                pH2=0,                                      #partial pressure of atmospheric hydrogen in bar
                pHe=0,                                      #partial pressure of atmospheric helium in bar
                pNe=0,                                      #partial pressure of atmospheric neon in bar
                pKr=0,                                      #partial pressure of atmospheric krypton in bar
                pH2O=0,                                     #partial pressure of atmospheric water (doesn't impact water cycle)
                wetsoil=True,                               #alters albedo of soil based on how wet it is
                vegetation=2,                               #toggles vegetation module; 1 for static vegetation, 2 to allow growth
                vegaccel=1,                                 #rate of vegetation growth
                initgrowth=0.5,                             #initial global vegetation cover
                glaciers={'toggle': True,                   #toggles glacier module
                          'mindepth': 2,                    #depth of snow requires to form glacier
                          'initialh': 0                    #initial global glacier cover; -1 for no initial glaciers
                         }
               )

#remember that you can delete parameters you don't need

model.cfgpostprocessor(times=12,  #number of output times (months) in the output files
                       extension='.nc')

model.exportcfg()   #saves the configuration settings in the config step, so you can just load that config in the future

model.runtobalance(baseline=10,   #number of years necessary to hold balance for
                   maxyears=750,  #maximum number of years to run
                   minyears=75,   #minimum number of years to run
                   timelimit=720, #maximum time to run, in minutes
                   clean=True     #removes unnecessary files between years
                  )

model.finalize('model_out',       #name of the output folder
               allyears=True,     #retain outputs (and restarts) of all years, rather than just the last one
               clean=True,        #delete the work directory
               keeprestarts=True  #move restart files as well as output files
              )

model.save()  #saves the current state of the model so it can be run further if necessary
