import ftplib, sys


def FTPUpload(locImgLoc, remoteImgName):
    
    ftpSess = ftplib.FTP()
    ftpSess.set_debuglevel(1)

    ftpSess.connect('159.89.121.6', 1511)
    ftpSess.login("icares", "avengers")

    with open(locImgLoc, 'rb') as fpr:
        ftpSess.storbinary('STOR ' + remoteImgName, fpr)

    ftpSess.quit()
