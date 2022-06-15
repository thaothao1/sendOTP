from utils.dbUtil import database
from otps import schema


def find_block_otp(recipient_id : str):
    query = "SELECT * FROM py_otp_blocks WHERE recipient_id:= recipient_id"\
            "AND created_on >= now() at time zone 'UTC' - interval '5 minutes'"
    
    return database.fetch_one(query , values={"recipient_id": recipient_id})

def save_otp(
        request : schema.CreateOTP,
        session_id : str,
        otp_code: str,
):
        query = "INSERT INTO py_otps VALUES(nextval('otp_id_seq'), :recipient_id , :session_id , :otp_code , '1' , now() at time zone 'UTC' , null , 0)" 
        return database.execute(query , values={"recipient_id"})

def find_otp_lifetime(
        request: schema
):
        query = "SELECT * FROM py_otps WHERE recipient_id=:recipient_id , and session_id=: session_id and "\
                "created_on >= now() at time zone 'UCT' - interval '1 minutes' "
        return database.fetch_one(query, values={"recipient_id": request.recipient_id  , "sesion_id": request.session_id})

def save_otp_failed_count(
        request: schema.OTPList
):
        query = "UPDATE py_otps SET otp_failed_count=otp_failed_count+1 where recipient_id=:recipient_id  "\
                "and session_id=:session_id and otp_code=: otp_code"
        return database.execute(query , values={"recipient_id": request.recipient_id, "session_id": request.session_id , "otp_code": request.otp_code})