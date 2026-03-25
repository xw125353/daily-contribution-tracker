import os
import subprocess
import random
from datetime import datetime, timedelta

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}\n{e.stderr}")
        return None

def create_contributions(repo_name, days=365, commits_per_day_range=(1, 5)):
    # Create a local directory for the repo
    repo_path = f"/home/ubuntu/{repo_name}"
    if os.path.exists(repo_path):
        run_command(f"rm -rf {repo_path}")
    os.makedirs(repo_path)
    
    os.chdir(repo_path)
    run_command("git init")
    
    # Configure git locally
    run_command('git config user.name "xw125353"')
    run_command('git config user.email "3540963809@qq.com"')
    
    current_date = datetime.now()
    start_date = current_date - timedelta(days=days)
    
    print(f"Generating contributions from {start_date.date()} to {current_date.date()}...")
    
    for i in range(days + 1):
        day = start_date + timedelta(days=i)
        
        # Randomly skip some days to look more natural (e.g., skip 10% of days)
        if random.random() < 0.1:
            continue
            
        num_commits = random.randint(commits_per_day_range[0], commits_per_day_range[1])
        
        for _ in range(num_commits):
            # Random time within the day
            hour = random.randint(9, 22)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            commit_date = day.replace(hour=hour, minute=minute, second=second)
            
            # Format: ISO 8601
            date_str = commit_date.strftime("%Y-%m-%dT%H:%M:%S")
            
            # Create/modify a file with some content to avoid empty commits
            with open("activity.log", "a") as f:
                f.write(f"Log entry for {date_str}\n")
            
            run_command("git add activity.log")
            
            # Set both GIT_AUTHOR_DATE and GIT_COMMITTER_DATE
            # The environment variables must be passed to the git commit command
            env_vars = f"GIT_AUTHOR_DATE='{date_str}' GIT_COMMITTER_DATE='{date_str}'"
            run_command(f"{env_vars} git commit -m 'Update activity log for {date_str}'")

    print(f"Finished generating local commits in {repo_path}.")

if __name__ == "__main__":
    REPO_NAME = "daily-contribution-tracker"
    create_contributions(REPO_NAME)
