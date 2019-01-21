# Contributing guidelines

* Language : english for all. Better for the project management and the "accent" management.

* To add a modification, create a new branch, and then ask for a pull request to put your modifications on master.

* Create a new branch only from `master`, to start from solid basis.

* Never perform a `git add .` or a `git add --all`, unless you know exactly what you are trying to do, in order to add only the files we wanted and not
save generated files like cache files. If a file was committed, it is quite difficult to erase him from the git history. Always perform `git add filename`

* When you review a branch, be careful to the possible generated files unwanted.

* Insert a reference of the issue in your commit, to simplify the verification process. ([Issue #XXX] Fix this... for example)

* Always commit with `git commit` and not `git commit -m`, to have a multi-lines commmit, to provide more informations.

Syntax :

```
[Issue #XXX] Short description of what we have done, starting with an action verb if possible and an uppercase

Blablabla
Blablabla
Blablabla
```
