from fastapi import APIRouter,status, HTTPException,Depends,Request, Form
from typing import List
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import schemas, models

models.Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory='templates')
router = APIRouter()

def get_db():
    db =SessionLocal()
    try:
        yield db
    finally:
        db.close()


# get all data without template
@router.get('/data/original')
async def home(request:Request,db: Session=Depends(get_db), ):
    retrive_all_data = db.query(models.Magician).all()
    return {'data' : retrive_all_data}
        
# get all data
@router.get('/data')
async def home(request:Request,db: Session=Depends(get_db), ):
    retrive_all_data = db.query(models.Magician).all()
    return templates.TemplateResponse('index.html', {'request':request, 'data' : retrive_all_data})


#create new data
@router.post('/add', status_code=status.HTTP_201_CREATED)
async def store_data(request: Request, fullname : str=Form(...),desc:str=Form(...),db:Session = Depends(get_db)):
    new_data = models.Magician(fullname=fullname, description = desc)
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    url = router.url_path_for('home')
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)

# get data by id
@router.get('/data/{id}')
async def get_data_by_id(id:int,db:Session=Depends(get_db)):
    get_by_id= db.query(models.Magician).filter(models.Magician.id == id).all()
    if not get_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog not {id} exist")
    return {'data' : get_by_id}

# delete data by id
@router.delete('/data/{id}',status_code=status.HTTP_204_NO_CONTENT)
async def delete_by_id(id :int, db:Session=Depends(get_db)):
    db.query(models.Magician).filter(models.Magician.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Done' :f"data {id} has deleted" }

@router.put('/data/{id}')
async def update_data(id:int, request:schemas.Magician, db:Session = Depends(get_db)):
    data = db.query(models.Magician).filter(models.Magician.id == id)
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with data id {id} not found")
    data.update({'fullname': request.fullname, 'description' : request.description})
    db.commit()
    return {"info" : 'Successfully'}