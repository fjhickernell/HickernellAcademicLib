# Instructor Workflow for Using HickernellClassLib with Course Repositories

This document describes the recommended development and synchronization workflow for using **HickernellClassLib** across multiple Macs and across multiple course repositories (e.g., MATH565Fall2025, MATH476, MATH563).

It ensures:

- One canonical version of HickernellClassLib  
- Clean and reproducible submodule versions for students  
- Ability to develop from any Mac  
- Smooth interaction with QMCSoftware (develop branch)  
- Avoids notebooks importing the wrong copy  

---

## 1. Canonical Source of Truth

The only editable copy of the library is located here on every Mac:

```
~/SoftwareRepositories/HickernellClassLib
```

All development edits should occur only in this clone and on the `main` branch.

To sync it:

```bash
cd ~/SoftwareRepositories/HickernellClassLib
git pull
```

Do **not** edit the `classlib/` folder inside course repos.

---

## 2. Install HickernellClassLib (editable) into the qmcpy Conda environment

On each Mac, run once:

```bash
conda activate qmcpy
cd ~/SoftwareRepositories/HickernellClassLib
pip install -e .
```

Benefits:

- `import classlib` loads the canonical version  
- All courses see the same version  
- No need for messing with `sys.path`  
- No stale imports from submodules  

Whenever you update the library for your own benefit:

```bash
git pull
pip install -e .   # usually unnecessary but safe
```

---

## 3. Course Repositories Use Submodules

Each course repo contains:

- `classlib` → submodule pointing to HickernellClassLib  
- `qmcpy` → submodule pointing to QMCSoftware *develop* branch  

### Students update with:

```bash
git pull
git submodule update --init --recursive
```

### Instructor updates the classlib submodule pointer

When you want students to receive the updated version:

```bash
cd ~/SoftwareRepositories/MATH565Fall2025
git submodule update --remote classlib
git add classlib
git commit -m "Update classlib submodule to latest HickernellClassLib"
git push
```

This ensures the course uses the exact version you select.

---

## 4. QMCSoftware (develop branch)

Course repos track the **develop** branch of QMCSoftware.

To update:

```bash
cd ~/SoftwareRepositories/MATH565Fall2025
git submodule update --remote qmcpy
git add qmcpy
git commit -m "Update qmcpy to latest develop"
git push
```

### Stability Philosophy

Your team develops in feature branches and only merges into `develop` after validation.  
Therefore:

- Updating your **own working copy** to the latest `develop` is safe and recommended.  
- Updating the **course repo** should still be intentional—only when you have verified the notebooks still run correctly.

If you need functionality not yet upstreamed:

- Temporarily implement it in HickernellClassLib  
- Or keep a temporary branch  
- Upstream later when appropriate  

---

## 5. Workflow Across Macs

You may edit HickernellClassLib from **any** Mac.

### On Mac A (where you make edits):

```bash
cd ~/SoftwareRepositories/HickernellClassLib
git add .
git commit -m "Work done"
git push
```

### On Mac B:

```bash
cd ~/SoftwareRepositories/HickernellClassLib
git pull
```

### To update the course repo afterward (optional):

```bash
cd ~/SoftwareRepositories/MATH565Fall2025
git submodule update --remote classlib
git add classlib
git commit -m "Update HickernellClassLib submodule"
git push
```

---

## 6. Why This Model Works

- Prevents unsynchronized library versions across Macs  
- Eliminates “wrong library imported” issues in Jupyter  
- Course repos remain clean snapshots for each semester  
- Students use stable, pinned versions  
- HickernellClassLib remains a general library across all courses  
- QMCSoftware develop remains stable but **course repo updates remain intentional**  

---

## 7. Daily Instructor Checklist

Before working on any course:

```bash
conda activate qmcpy
cd ~/SoftwareRepositories/HickernellClassLib
git pull
pip install -e .

cd ~/SoftwareRepositories/MATH565Fall2025
git pull
git submodule update --init --recursive
```

When you want students to receive updates:

```bash
cd ~/SoftwareRepositories/MATH565Fall2025
git submodule update --remote classlib
git add classlib
git commit -m "Update HickernellClassLib version"
git push
```

When you want students to receive a newer QMCSoftware develop:

```bash
git submodule update --remote qmcpy
git add qmcpy
git commit -m "Update qmcpy to latest develop"
git push
```

---

