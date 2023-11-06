
# Backend

cd backend/src
pip install -r requirements

## start app
uvicorn main:app --reload --host 0.0.0.0 --port 8000
## run tests
uvicorn main:app --reload --host 0.0.0.0 --port 8000


# Frontend

cd frontend
yarn install

## start app
yarn start

## Storybook / tests 
yarn storybook


