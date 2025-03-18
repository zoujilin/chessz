:: NOT run in windows powershell
doskey diff=FC /N $*
doskey cat=type $*
doskey rm=del $*
doskey vi=notepad $*
doskey ll=dir
doskey gss=git status -s
doskey gll=git pull
doskey ghh=git push 
doskey gmm=git commit -m $*
doskey gaa=git add $*
doskey gdf=git diff $*
doskey gco=git checkout $*
doskey gls=git ls-files
doskey bcp="C:\Program Files (x86)\Beyond Compare 3\bcompare.exe" $*

date /t
:: env to add path
:: in dos, rd img    // just delete a folder named img
:: git config --list
:: git config --global init.defaultbranch main
:: git commit -m "massage"

