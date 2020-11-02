## Dependencies
import logging
## Other .py files
import LoggerFunction

def renamer(siteName,searchTitle,filename_type,ResultsMatrix,pref_ID,pref_StripSymbol,WorkingDir):
    ## Basic Log Configuration
    logger = LoggerFunction.setup_logger('Renamers', '.\\Logs\\Watchdog.log',level=logging.INFO,formatter='%(asctime)s : %(name)s : %(levelname)-8s : %(message)s')
    ## Scene Logger information
    SceneNameLogger = LoggerFunction.setup_logger('SceneNameLogger', '.\\Logs\\'+searchTitle+'.log',level=logging.DEBUG,formatter='%(message)s')
    ## Calculate new filename section using sorted ResultMatrix
    logger.info ("********************* Renamer Function *********************")
    logger.info ("Calculating new filename based on your preferences and the available information")
    if (ResultsMatrix[0][5] == 0):
        logger.info ("Results Matrix had the declaration line first. This either suggests that the Matrix wasn't sort properly or didn't return any results for: " +searchTitle)
        logger.info ("******************** Return to Watchdog ********************")
        SceneNameLogger.handlers.pop()
        logger.handlers.pop()
        new_filename = None
    else:
        ID = ResultsMatrix[0][0]
        Title = ResultsMatrix[0][1]
        Date = ResultsMatrix[0][2]
        Actors = ResultsMatrix[0][3]
        Subsite = ResultsMatrix[0][4]
        if ((ID == '') and (pref_ID == True)):
            logger.info ("The site didn't provide a sceneID")
            logger.info ("Will use a SiteName - Title scheme based on your preferences")
            if (pref_StripSymbol != ''):
                if (Date != ''):
                    if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+' '+pref_StripSymbol+' '+Actors+' - '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3]+' - '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+' '+pref_StripSymbol+' '+Actors+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                        new_filename = siteName+' - '+Date+' - '+Time+' '+pref_StripSymbol+' '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                else:
                    if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                        new_filename = siteName+' - '+Title+' '+pref_StripSymbol+' '+Actors+' - '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3]+' - '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                        new_filename = siteName+' - '+Title+' '+pref_StripSymbol+' '+Actors+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                        new_filename = siteName+' - '+Title+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                        new_filename = siteName+' - '+Title+' '+pref_StripSymbol+' '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
            else:
                if (Date != ''):
                    new_filename = siteName+' - '+Date+' - '+Title+filename_type
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                    for y in range (len(ResultsMatrix)-1):
                        SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1])
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")                    
                else:
                    new_filename = siteName+' - '+Title+filename_type
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                    for y in range (len(ResultsMatrix)-1):
                        SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1])
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")  
        elif ((ID != '') and (pref_ID == True)):
            if (pref_StripSymbol != ''):
                if (Date != ''):
                    if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                        new_filename = siteName+' - '+Date+' - '+ID+' '+pref_StripSymbol+' '+Actors+' - '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][0]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3]+' - '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                        new_filename = siteName+' - '+Date+' - '+ID+' '+pref_StripSymbol+' '+Actors+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][0]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                        new_filename = siteName+' - '+Date+' - '+ID+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][0])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                        new_filename = siteName+' - '+Date+' - '+ID+' '+pref_StripSymbol+' '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][0]+' '+pref_StripSymbol+' '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                else:
                    if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                        new_filename = siteName+' - '+ID+' '+pref_StripSymbol+' '+Actors+' - '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][0]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3]+' - '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                        new_filename = siteName+' - '+ID+' '+pref_StripSymbol+' '+Actors+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][0]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                        new_filename = siteName+' - '+ID+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][0])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                        new_filename = siteName+' - '+ID+' '+pref_StripSymbol+' '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][0]+' '+pref_StripSymbol+' '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
            else:
                if (Date != ''):
                    new_filename = siteName+' - '+Date+' - '+ID+filename_type
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                    for y in range (len(ResultsMatrix)-1):
                        SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][0])
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")                    
                else:
                    new_filename = siteName+' - '+ID+filename_type
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                    for y in range (len(ResultsMatrix)-1):
                        SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][0])
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")                   
        else:
            if (pref_StripSymbol != ''):
                if (Date != ''):
                    if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+' '+pref_StripSymbol+' '+Actors+' - '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3]+' - '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+' '+pref_StripSymbol+' '+Actors+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                        new_filename = siteName+' - '+Date+' - '+Title+' '+pref_StripSymbol+' '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                else:
                    if (Actors != '' and Subsite != ''): ## We have information for actors and Subsite
                        new_filename = siteName+' - '+Title+' '+pref_StripSymbol+' '+Actors+' - '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3]+' - '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors != '' and Subsite == ''): ## We have information for actors and not for Subsite
                        new_filename = siteName+' - '+Title+' '+pref_StripSymbol+' '+Actors+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][3])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite == ''): ## We don't have information for actors and Subsite
                        new_filename = siteName+' - '+Title+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    elif (Actors == '' and Subsite != ''): ## We don't have information for actors but we have for Subsite
                        new_filename = siteName+' - '+Title+' '+pref_StripSymbol+' '+Subsite+filename_type
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                        SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                        for y in range (len(ResultsMatrix)-1):
                            SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1]+' '+pref_StripSymbol+' '+ResultsMatrix[y][4])
                        SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
            else:
                if (Date != ''):
                    new_filename = siteName+' - '+Date+' - '+Title+filename_type
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                    for y in range (len(ResultsMatrix)-1):
                        SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][2]+' - '+ResultsMatrix[y][1])
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")                    
                else:
                    new_filename = siteName+' - '+Title+filename_type
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
                    SceneNameLogger.debug ("If your scene was in results but the Watchdog mismatched it then use as filename the matched one from below")
                    for y in range (len(ResultsMatrix)-1):
                        SceneNameLogger.debug(siteName+' - '+ResultsMatrix[y][1])
                    SceneNameLogger.debug ("************** Scene in Result but Mismatched **************")
        ## logger.debug new filename
        logger.info ("*************** After-Process filename section *************")
        logger.info ("The new filename is: " +new_filename)
        logger.info ("******************** Return to Watchdog ********************")
        SceneNameLogger.handlers.pop()
        logger.handlers.pop()
    return new_filename