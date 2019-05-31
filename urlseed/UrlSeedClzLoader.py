from urlseed.GetLawyerInArea import GetLawyerInArea;
from urlseed.GetPageSize import GetPageSize;

from urlseed.ToGetImage import ToGetByte;
from urlseed.ToGetLawyerDetail import ToGetLawyerDetail;
from urlseed.ToGetLawyerInfo import ToGetLawyerInfo;
from urlseed.ToGetOfficeDetail import ToGetOfficeDetail;



# from urlseed.ToGetLawyerInfo import ToGetLawyerInfo


def getClassList():
    return {
        "GetLawyerInArea":GetLawyerInArea,
        "GetPageSize":GetPageSize,
        "ToGetByte":ToGetByte,
        "ToGetLawyerDetail":ToGetLawyerDetail,
        "ToGetLawyerInfo":ToGetLawyerInfo,
        "ToGetOfficeDetail":ToGetOfficeDetail}

def  getSeedClass():
#       return [ToGetLawyerDetail]
     return [GetLawyerInArea]