import uvicorn
from sys import prefix

from internal.controller.ApiUserController import routerUser
from internal.controller.ApiUserContestController import routerUserContest
from internal.controller.ApiUserStatementController import routerUserStatement
from internal.controller.ApiAdminController import routerAdmin
from internal.controller.ApiOnlineAuditoriumController import routerOnlineAuditorium
from internal.controller.ApiOnlineAuditoriumMessageController import routerOnlineAuditoriumMessage
from internal.controller.ApiTestController import routerTest
from internal.controller.ApiUserExpertStatementGradeController import routerUserExpertStatementGrade


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    ...
]
app.add_middleware(
   CORSMiddleware,
   allow_origins=origins,
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

app.include_router(routerUser, prefix="/api/user")
app.include_router(routerUserContest, prefix="/api/user/contest")
app.include_router(routerUserStatement, prefix="/api/user/statement")
app.include_router(routerAdmin, prefix="/api/admin")
app.include_router(routerOnlineAuditorium, prefix="/api/online_auditorium")
app.include_router(routerOnlineAuditoriumMessage, prefix="/api/online_auditorium_message")
app.include_router(routerUserExpertStatementGrade, prefix="/api/user_expert_statement_grade")

@app.get("/api")
def index():
    return {"status":"success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8092)
