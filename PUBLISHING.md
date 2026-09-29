# Publishing checklist

Follow these steps to put Stemsyl online and on the public record as prior art. Nothing here costs money.

## 1. Before you publish

- [ ] Check your name as it should appear. It is in `AUTHORS.md`, `CITATION.cff`, `SPECIFICATION.md` (the title block, section 10 and How to cite), `README.md`, `docs/index.html` (the footer and the author tag), and `AUTHOR` in `tools/spec.py`. After any change, run `python3 tools/rebuild.py` to remake the web page and the PDF.
- [ ] Read the PDF, `docs/stemsyl-specification.pdf`, from start to finish. It is the document the prior-art date will attach to.
- [ ] Run `python3 tools/rebuild.py --test`. Everything should pass.

## 2. Put it on GitHub

1. Sign in at [github.com](https://github.com) and create a new public repository named `stemsyl`. Don't add a README or licence, since this folder has its own.
2. Upload the contents of this folder. Two ways:
   - **In the browser:** on the new repository's page, choose "uploading an existing file" and drag in every file and folder. There are 78 files, within GitHub's limit of 100 files per upload, and every file is under its 25 MB limit for browser uploads. The largest are the word list (14 MB) and the two keyboards (4 MB each). Two files have names starting with a dot, `.gitignore` and `docs/.nojekyll`, and your computer may hide them. They are useful but not essential.
   - **With git:**

     ```sh
     git init && git add . && git commit -m "Stemsyl 1.0"
     git branch -M main
     git remote add origin https://github.com/YOUR-USERNAME/stemsyl.git
     git push -u origin main
     ```
3. On the repository page, click the gear next to **About**. Add a description ("A colour-stem phonetic script for English, with keyboards for phones and watches") and these topics: `writing-system`, `phonetics`, `keyboard`, `smartwatch`, `accessibility`.

## 3. Turn on the website (GitHub Pages)

1. In the repository, go to **Settings → Pages**.
2. Under **Build and deployment**, choose **Deploy from a branch**, then branch `main` and folder `/docs`, and save.
3. After a minute or two the site is at `https://YOUR-USERNAME.github.io/stemsyl/`. There, `index.html` is the front page, and the apps, the specification and the PDF are one click away. The file `docs/.nojekyll` tells GitHub to serve the files as they are.
4. Put the site's address in the repository's **About** box, and at the top of `README.md`.

## 4. Publish the specification as prior art

A defensive publication is a public, dated disclosure. Once it exists, no one can patent what it describes. Do both of the following. Each is free.

### Technical Disclosure Commons (tdcommons.org)

Technical Disclosure Commons publishes defensive disclosures free of charge. It dates each one, and it lets search tools, including Google Patents, index them, so patent examiners can find them.

1. Create an account at [tdcommons.org](https://www.tdcommons.org/) and choose **Submit a Defensive Publication**.
2. Title: *Stemsyl: a colour-stem phonetic script for English, with keyboards for phones and watches*.
3. Author: your name. You may publish anonymously, but then your name can't be searched.
4. Abstract: copy the Abstract section from `SPECIFICATION.md`.
5. File: upload `docs/stemsyl-specification.pdf`.
6. Submit. It can take up to 72 hours to appear. Keep its web address; the date on it is your prior-art date.

### Zenodo (zenodo.org)

Zenodo, run by CERN, gives each upload a permanent DOI.

1. Sign in at [zenodo.org](https://zenodo.org/), for example with your GitHub account.
2. Choose **New upload** and add `docs/stemsyl-specification.pdf`.
3. Resource type: *Publication / Technical note*. Title and author as above; the description is the abstract; licence *Creative Commons Zero v1.0 Universal*.
4. Publish, and note the DOI.
5. You can also archive the software. In Zenodo's GitHub settings, switch on the `stemsyl` repository, then make a release on GitHub (for example `v1.0`). Zenodo will archive it with its own DOI, reading `CITATION.cff` for the title and author.

### Afterwards

- Add the Technical Disclosure Commons address and the DOI to "How to cite" in `SPECIFICATION.md`, to `README.md` and to `CITATION.cff` (as `doi:`), and run `python3 tools/rebuild.py`.
- **Each time you add a feature, publish again.** Prior art protects only what was disclosed, as of the day it was disclosed. When the apps gain something new, describe it in `SPECIFICATION.md`, raise the version, and publish that version:
  - on Zenodo, as a new version of the same record
  - on Technical Disclosure Commons, as a new submission

## 5. Optional

- **The name.** Search the USPTO's trademark database (and others where you care) for "Stemsyl" before you rely on the name. Registering it as a trademark is possible, but it costs money and is not needed to keep the ideas free.
- **Apple's App Store.** The Free Software Foundation considers the App Store's terms incompatible with the GPL, and VLC was removed from the store over this in 2011. As the copyright holder, you can still publish your own app there, because a licence does not bind its own author. If other people contribute code under the GPL, however, you would need their permission too. If you plan to ship on the App Store and accept contributions, you could add a GPL section 7 "additional permission" for app stores now. That would need careful wording; this is not legal advice.
- **A native watch app.** Apple Watch runs native watchOS apps, not web pages. The watch keyboard here is a complete working model to build one from: its layout, its timings and its behaviour are all in section 5.4 of the specification.
