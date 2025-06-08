from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, cache, search

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/{product_id}", response_model=schemas.ProductSchema)
def read_product(product_id: int, db: Session = Depends(get_db)):
    cached = cache.cache_get(f"product:{product_id}")
    if cached:
        return schemas.ProductSchema.parse_raw(cached)

    db_product = crud.get_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    cache.cache_set(f"product:{product_id}", schemas.ProductSchema.from_orm(db_product).json())
    return db_product

@app.get("/products", response_model=list[schemas.ProductSchema])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/search/")
def search(query: str):
    results = search.search_products(query)
    return results["hits"]["hits"]



# MYSQL_URL=mysql+pymysql://user:password@localhost:3306/ecommerce
# REDIS_HOST=localhost
# REDIS_PORT=6379
# ES_HOST=http://localhost:9200
