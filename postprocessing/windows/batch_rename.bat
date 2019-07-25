:: Set the SORC folder location to the root folder containing all/some other folders.
:: E.g if your videos are C:\triplex\DigitalPlayground.18.12.12.Elsa.Jean.And.Romi.Rain.The.Secret.Life.Of.A.Housewife.XXX.1080p.MP4-KTRR\askdfjugbdsf7afuba9d8fbha.mp4
:: use "C:\triplex\*"
:: if you only want to do one studio or even just one video change the wildcard e.g "C:\triplex\DigitalPlayground*"

:: change the -d argument to -b if you experience permissions issues with the log file (setup in other files)
:: delete the -d argument to turn off dry run mode
:: add -c argument to enable cleanup of leftover files and folders


SET SORC="P:\Path\To\Folders\optional_wildcard*"
SET SCRIPT="C:\Path\To\pa_renamer_post.py"
SET PROG="C:\Python27\python.exe"

FOR /f "tokens=*" %%G in ('dir /b /s /a:d %SORC%') DO (
    %PROG% %SCRIPT% -d "%%G" )
pause
