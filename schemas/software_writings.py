from pydantic import BaseModel

class SoftwareWritings(BaseModel):
    software_name: str = ""                   # 软件名称
    registration_number: str = ""             # 登记号
    acquisition_method: str = ""              # 权利取得方式
    department: str = ""                      # 部门
    team: str = ""                            # 团队
    development_completion_date: str = ""     # 开发完成日期
    registration_date: str = ""               # 登记日期
    copyright_owners: str = ""                # 著作权人（多人用逗号分隔）