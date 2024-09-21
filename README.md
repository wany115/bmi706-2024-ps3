# bmi706-2023-ps3

Hello, Yuan Wang!


## Requirements

Please make sure to have the following downloaded and installed on your machine before proceeding.

- [Visual Studio Code](https://code.visualstudio.com/download)
- [Git](https://git-scm.com/download)
- [Anaconda](https://docs.anaconda.com/anaconda/install/)

> If you have a preferred text editor and/or know how to manage python virtual environments, please view these requirements
as recommendations.

### Getting started

#### Create **private** GitHub repo from `hms-dbmi/bmi706-2023-ps3`

In order to work independently of your classmates, we ask that you create a **private GitHub repository** for this template repo.
Select the **Download ZIP** option to download the archive for this folder.

<img src="https://user-images.githubusercontent.com/24403730/217667978-78e2de3b-82dc-425a-8fb4-473d3bcd6737.png">

Unzip the archive and drag the folder into VS Code. Within VS Code, select the **Source Control** and **Publish to GitHub**.
Modify the name in the prompt at the top of the editor to `bmi706-2023-ps3`, and select **Publish to GitHub Private repository**.

<img src="https://user-images.githubusercontent.com/24403730/217669894-b1e4cfa2-7b30-44cd-b3d1-2fc2e1568cfb.png">


This will create a private GitHub repository under `<YOUR-GITHUB-USERNAME>/bmi706-2023-ps3`. This step is essential for eventually
sharing your application on Streamlit Cloud.

#### Making changes

You can now open your initialized project in VS Code and begin editing.

<img src="https://user-images.githubusercontent.com/24403730/217671131-bdf8b3cc-ba86-4ba0-8dd9-e599a8172685.png">

Selecting a file from the sidebar will open the file in the editor where you are free make changes.

#### Committing changes

A *commit* is a snapshot of the state of your repository at a specific time. Git keeps track of history of
your repository via commits so that you can revert back to a prior version at any time. In order to
synchronize your local changes with the fork on GitHub, you will need to create a *new commit* 
adding the changes you've made. 

Let's practice making a commit by replacing "Hello, world" with "Hello, `<your name>`" at the top of this file.

- Open `README.md` in VS Code.

<img src="https://user-images.githubusercontent.com/24403730/217670989-5d94455d-65b2-4c42-a1d7-643575ea43eb.png">

- Replace `world` at the top of the file with *your name* and save the file.

<img src="https://user-images.githubusercontent.com/24403730/217670993-a5a0ce45-de8e-4e7c-90ae-e931342bea8d.png">

> Note how the file tab for `README.md` is now yellow with an "M", signifing that it has been modified. The **Source Control** icon in the 
> sidebar additionally has shows a `1`, indicating that `1` file has changed.

- Click the **Source Control** icon in the sidebar and enter *Message* describing the changes we've made. Click the 
"Commit" check mark to stage and commit our changes.

<img src="https://user-images.githubusercontent.com/24403730/217671484-9d1f2fa9-d73f-4058-923e-fabba4cea87e.png">

- Click the Synchronize Changes to update GitHub with our latest changes

<img src="https://user-images.githubusercontent.com/24403730/217671709-2c7bc25b-4e1c-45be-b505-f40058e0c2b9.png">

### Developing with `streamlit`

You'll need to set up a Python environment for working your Streamlit application locally. Streamlit's only officially-supported environment
manager on Windows, macOS, and linux is [Anaconda Navigator](https://docs.anaconda.com/anaconda/navigator/). Please make sure you 
have this installed. (The following is adapted from Streamlit's [documentation](https://docs.streamlit.io/library/get-started/installation).)

#### Create a new Python environment with Streamlit

1.) Follow the steps provided by Anaconda to
[set up and manage your environment](https://docs.anaconda.com/anaconda/navigator/getting-started/#managing-environments) 
using the Anaconda Navigator.

2.) Select the "▶" icon next to your new environment. Then select "Open terminal":

<img width="1024" src="https://i.stack.imgur.com/EiiFc.png">


3.) In the terminal that appears, type:

```bash
pip install streamlit
```

4.) Test that the installation worked:

```bash
streamlit hello
```

Streamlit's Hello app should appear in a new tab in your web browser.


#### Use your new environment

1.) In Anaconda Navigator, open a terminal in your environment (see step 2 above).

2.) In the terminal that appears, navigate to your local workspace and run:

```bash
streamlit run streamlit_app.py
```

This will open the template streamlit app in the web browser. You can now start editing the contents
of `streamlit_app.py`, and refresh the page in your web browser we see changes.
