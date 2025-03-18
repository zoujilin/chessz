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
date /t
:: log some
:: in dos, rd img    // just delete a folder named img
:: git config --list
:: git config --global init.defaultbranch main
:: git commit -m "massage"

