# Team Contributions & Structure

## Project: Web Attendance Tracker
**Deadline:** June 18, 2026, 23:59
**Team Size:** 4 Members

---

## 👥 Team Members & Roles

### 1. Backend Developer
**Responsibilities:**
- Develop FastAPI REST API endpoints
- Implement database models using SQLAlchemy
- Create request/response schemas with Pydantic
- Handle authentication (if needed)
- Write API documentation
- Unit testing for backend

**Tasks:**
- [ ] Set up FastAPI project structure
- [ ] Create database models (Attendance, User, etc.)
- [ ] Implement CRUD endpoints
- [ ] Add filtering and search functionality
- [ ] Create error handling middleware
- [ ] Write tests
- [ ] Document API endpoints

**Files to work on:**
- `backend/app/main.py`
- `backend/app/models.py`
- `backend/app/routes.py`
- `backend/app/schemas.py`
- `backend/app/database.py`

**Submission deadline:** June 12

---

### 2. Frontend Developer
**Responsibilities:**
- Develop HTML/CSS/JavaScript interface
- Implement CRUD forms
- Create data tables with filtering
- Ensure responsive design (mobile-friendly)
- Integrate with backend API
- Frontend testing

**Tasks:**
- [ ] Create main HTML structure
- [ ] Design CSS styling (modern UI)
- [ ] Implement form validation
- [ ] Create attendance table
- [ ] Add search/filter functionality
- [ ] Implement edit modal
- [ ] Add delete confirmation
- [ ] Test all API integrations
- [ ] Ensure responsive design

**Files to work on:**
- `frontend/index.html`
- `frontend/style.css`
- `frontend/script.js`
- `frontend/pages/*`

**Submission deadline:** June 12

---

### 3. DevOps & Database Developer
**Responsibilities:**
- Set up PostgreSQL database
- Create Docker and Docker Compose configurations
- Manage database migrations
- Set up environment variables
- Ensure database optimization
- Deploy to Docker

**Tasks:**
- [ ] Initialize PostgreSQL database
- [ ] Create database schema
- [ ] Write Dockerfile for backend
- [ ] Write Dockerfile for Go service
- [ ] Create docker-compose.yml
- [ ] Set up environment configurations
- [ ] Create .env.example
- [ ] Test Docker deployment
- [ ] Document deployment process

**Files to work on:**
- `docker-compose.yml`
- `backend/Dockerfile`
- `go-service/Dockerfile`
- `.env.example`
- `DEPLOYMENT.md`

**Submission deadline:** June 12

---

### 4. AI/ML & QA Developer
**Responsibilities:**
- Develop attendance prediction model
- Implement anomaly detection
- Create analytics endpoints
- Testing and quality assurance
- Create comprehensive documentation
- Generate demo video

**Tasks:**
- [ ] Create prediction model
- [ ] Implement anomaly detection algorithm
- [ ] Create analytics calculations
- [ ] Integrate AI/ML with backend API
- [ ] Perform comprehensive testing
- [ ] Create test report
- [ ] Write project documentation
- [ ] Create demo video (3-5 minutes)
- [ ] Create contribution table
- [ ] Prepare final report

**Files to work on:**
- `ai-module/predictor.py`
- `ai-module/anomaly_detector.py`
- `backend/app/routes.py` (AI endpoints)
- Documentation files
- Demo video

**Submission deadline:** June 16 (for report and video)

---

## 📅 Timeline

| Date | Milestone | Owner |
|------|-----------|-------|
| June 4 | GitHub Classroom setup, database schema | DevOps |
| June 6 | Backend API initial version | Backend Dev |
| June 8 | Frontend UI initial version | Frontend Dev |
| June 10 | Docker setup complete | DevOps |
| June 12 | Core functionality complete | Backend + Frontend |
| June 14 | AI/ML integration, full testing | AI/ML Dev |
| June 15 | Bug fixes and optimization | All |
| June 16 | Report and video ready | QA/AI Dev |
| June 18 | Final submission | All

---

## 🔄 Collaboration Guidelines

### Git Workflow
1. Create feature branches: `git checkout -b feature/your-feature`
2. Commit regularly: `git commit -m 'Clear message'`
3. Push to your branch: `git push origin feature/your-feature`
4. Create Pull Request for review
5. Merge after approval

### Communication
- Daily stand-ups (5 min)
- Weekly progress reviews
- Use GitHub issues for tracking tasks
- Slack/Discord for quick communication

### Code Standards
- Python: PEP 8
- Go: gofmt
- JavaScript: Use const/let, avoid var
- HTML: Semantic HTML5
- CSS: BEM naming convention

---

## 📊 Contribution Table

**To be filled in during final submission:**

| Member Name | Role | Tasks Completed | % Contribution | Hours Worked |
|-------------|------|-----------------|-----------------|---------------|
| Member 1 | Backend | [ ] | 25% | __ |
| Member 2 | Frontend | [ ] | 25% | __ |
| Member 3 | DevOps/DB | [ ] | 25% | __ |
| Member 4 | AI/ML/QA | [ ] | 25% | __ |
| **TOTAL** | | | **100%** | **__** |

---

## 📝 Final Submission Checklist

**Team Lead to submit:**
- [ ] GitHub repository link
- [ ] Private repo with @bakhtiyar-k as collaborator
- [ ] Project Report (PDF) - 6-12 pages
  - [ ] Title page
  - [ ] Team members and contributions
  - [ ] Project overview
  - [ ] Problem statement
  - [ ] Methodology/Tools
  - [ ] Main features description
  - [ ] Implementation explanation
  - [ ] Screenshots
  - [ ] Testing/Evaluation results
  - [ ] Difficulties and solutions
  - [ ] Conclusion
  - [ ] GitHub and demo links
- [ ] Demo Video (3-5 minutes) - shows:
  - [ ] GitHub repository
  - [ ] Project running
  - [ ] Main features
  - [ ] Team contributions
- [ ] Contribution table (filled)

**Deadline: June 18, 2026, 23:59**

---

## 🎯 Success Criteria

✅ All core CRUD features working
✅ Clean, responsive UI
✅ AI predictions functional
✅ Docker deployment working
✅ Code is well-documented
✅ All tests passing
✅ Demo video shows all features
✅ Report is comprehensive

Good luck! 🚀
