from fastapi import APIRouter , HTTPException , status
from otps import schema
from enums import otps
from otps import crud
from utils import otpUtil
import uuid


router = APIRouter(prefix="/api/v1")

@router.post("/otp/send")
async def send_otp(
    type : otps.OTPType,
    request: schema.CreateOTP
):

    #check block OTP
    otp_blocks = await crud.find_block_otp(request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Sorry , this phone number is blocked in 5 minutes.")

    #Generate and save to table py_otps
    otp_code = otpUtil.random(6)
    session_id = str(uuid.uuid1())
    await crud.save_otp(request, session_id , otp_code)
    return "sending OTP "

@router.post("/otp/verify")
async def send_verify(request: schema.VerifyOTP):
    #check block OTP
    otp_blocks = await crud.find_block_otp(request.recipient_id)
    if otp_blocks:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail = "sorry")
    lifetime_result = await crud.find_otp_lifetime(request)
    if not lifetime_result.status == "9":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "OTP code has expired , please")

    #Verify OTP  code,
    #if not verified
    if lifetime_result.otp_code != request.otp_code:
        await crud.save_otp_failed_count(lifetime_result)
         


    return "sending OTP"