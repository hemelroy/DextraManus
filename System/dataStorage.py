import sqlite3
import bcrypt

class StorageManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name) #e.g. "records.db"
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS Password (username text, password text)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS ModelSettings (profileId integer NOT NULL, modelComplexity integer, minDetectionConf real, minTrackConf real)")
        self.conn.commit()
        #self.conn.close()

        #Verify if password exists. If not initialize with default password
        #self.conn = sqlite3.connect("records.db")
        #self.cur = conn.cursor()
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM Password WHERE username=?)", ("Admin",))
        self.exists = self.cur.fetchall()[0][0]
        if not self.exists:
            # Encode the stored password:
            self.password = "V&V2022"
            self.password = self.password.encode('utf-8')
            # Encrypt the stored pasword:
            self.hashed = bcrypt.hashpw(self.password, bcrypt.gensalt(10))

            self.cur.execute("INSERT INTO Password VALUES (?,?)",("Admin", self.hashed,))
            self.conn.commit()

        #Verify if model parameters have been added. If not, initialize with default
        self.cur.execute("SELECT EXISTS(SELECT 1 FROM ModelSettings WHERE profileId=?)", (1,))
        self.exists = self.cur.fetchall()[0][0]
        if not self.exists:
            self.cur.execute("INSERT INTO ModelSettings VALUES (?,?,?,?)",(1, 1, 0.5, 0.5,))
            self.conn.commit()

        self.conn.close()
        #Model complexity - Complexity of the hand landmark model: 0 or 1. Landmark accuracy as well as inference latency generally go up with the model 
        # complexity. Default to 1

        #MIN_DETECTION_CONFIDENCE
        #Minimum confidence value ([0.0, 1.0]) from the hand detection model for the detection to be considered successful. Default to 0.5.

        # MIN_TRACKING_CONFIDENCE:
        # Minimum confidence value ([0.0, 1.0]) from the landmark-tracking model for the hand landmarks to be considered tracked successfully, or otherwise hand 
        # detection will be invoked automatically on the next input image. Setting it to a higher value can increase robustness of the solution, at the expense of a 
        # higher latency. Ignored if static_image_mode is true, where hand detection simply runs on every image. Default to 0.5

    
    def authenticateUser(self, input):
        #Connect to database and grab hashed password for admin
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT password FROM Password WHERE username =?",("Admin",))  
        hashed = self.cur.fetchall()[0][0]
        input = input.encode('utf-8') 
        self.conn.close()

        #Compare provided input to the hashed password and return whether or not there's a match
        if bcrypt.checkpw(input, hashed):
            return True
        else:
            return False

    #Return -1 for mismatch between new password and confirmation, 0 for wrong old pass, 1 for successful update
    def changePassword(self, old_pass, new_pass, new_pass_ver):
        if (new_pass != new_pass_ver):
            return -1

        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("SELECT password FROM Password WHERE username =?",("Admin",))
        hashed = self.cur.fetchall()[0][0]
        old_pass = old_pass.encode('utf-8')

        #Compare provided input to the hashed password and return whether or not there's a match
        if not bcrypt.checkpw(old_pass, hashed):
            self.conn.close()
            return 0

        new_pass = new_pass.encode('utf-8')
        # Encrypt the stored pasword:
        new_pass = bcrypt.hashpw(new_pass, bcrypt.gensalt(10))

        self.cur.execute("UPDATE Password set password=? WHERE username=?", (new_pass,"Admin"))
        self.conn.commit()
        self.conn.close()

        return 1

    
    def verifyInputIntegrity(self, model_complexity, min_det_conf, min_track_conf):
        #Check if expected types are wrong
        if not (isinstance(model_complexity, int) and (isinstance(min_det_conf, float) or isinstance(min_det_conf, int)) 
            and (isinstance(min_track_conf, float) or isinstance(min_track_conf, int))):
            return False

        #Verify correct ranges
        if model_complexity != 0 and model_complexity != 1:
            return False
        elif min_det_conf < 0 or min_det_conf > 1:
            return False
        elif min_track_conf < 0 or min_track_conf > 1:
            return False

        return True

    #Return True if successful, False if there is an issue in provided inputs
    def modifyModelParams(self, model_complexity=1, min_det_conf=0.5, min_track_conf=0.5):
        
        if not self.verifyInputIntegrity(model_complexity, min_det_conf, min_track_conf):
            return False

        #Update parameters
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("UPDATE ModelSettings set modelComplexity=?, minDetectionConf=?, minTrackConf=? WHERE profileId=?", (model_complexity, min_det_conf, min_track_conf, 1))
        self.conn.commit()
        self.conn.close()
        return True

    def getModelParams(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute("Select modelComplexity, minDetectionConf, minTrackConf FROM  ModelSettings WHERE profileId=?", (1,))
        results = self.cur.fetchall()[0]
        self.conn.close()

        return results

        


stor = StorageManager("settings.db")

# print(stor.authenticateUser("123"))
# print(stor.authenticateUser("1234"))

# print(stor.changePassword('123', '1234', '11'))
# print(stor.changePassword('1234', '1234', '1234'))
# print(stor.changePassword('123', '1234', '1234'))

# print(stor.authenticateUser("1234"))

# print(stor.modifyModelParams())
# print(stor.modifyModelParams(model_complexity=-1))
# print(stor.modifyModelParams(min_det_conf='ds'))

print(stor.getModelParams())