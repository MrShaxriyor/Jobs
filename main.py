from fastapi import FastAPI
from schemas import Job
from database import cursor, conn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Job API with DB 🔥"}

@app.get("/jobs")
def get_jobs():
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()

    jobs = []
    for item in data:
        jobs.append({
            "id": item[0],
            "title": item[1],
            "company": item[2],
            "salary": item[3],
            "description": item[4]
        })
    return jobs

@app.post("/jobs")
def create_job(job: Job):
    cursor.execute(
        "INSERT INTO jobs(title, company, salary, description) VALUES(?,?,?,?)",
        (job.title, job.company, job.salary, job.description)
    )
    conn.commit()
    return {"message": "Job saved to database ✅"}


@app.get("/jobs/{job_id}")
def get_single_job(job_id: int):
    cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
    job = cursor.fetchone()

    if job is None:
        return {"error": "Job not found"}

    return {
        "id": job[0],
        "title": job[1],
        "company": job[2],
        "salary": job[3],
        "description": job[4]
    }

@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()

    return {"message": "Job deleted ✅"}

@app.put("/jobs/{job_id}")
def update_job(job_id: int, job: Job):
    cursor.execute(
        "UPDATE jobs SET title=?, company=?, salary=?, description=? WHERE id=?",
        (job.title, job.company, job.salary, job.description, job_id)
    )
    conn.commit()

    return {"message": "Job updated 🔥"}