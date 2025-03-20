from fastapi import FastAPI
from models.models import create_athlete_table, create_user_table, create_performance_table
from endpoints import sign_up, connexion, performance, athlete, statistics
from endpoints import sign_up, connexion, athlete, modification_user


app = FastAPI()

app.include_router(sign_up.router)
app.include_router(connexion.router)
app.include_router(performance.router)
app.include_router(athlete.router)
app.include_router(statistics.router)
app.include_router(modification_user.router)

@app.on_event("startup")
def on_startup():
    """
    Initializes the application by creating necessary database tables.

    This function is called at the startup of the application to ensure that
    the database tables for athletes, performances, and users are created.
    """
    create_athlete_table(), create_performance_table(), create_user_table()

# Lancer le serveur
if __name__ == "__main__":
    import uvicorn
    print("Démarrage de l'API...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
