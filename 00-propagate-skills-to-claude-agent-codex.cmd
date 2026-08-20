@echo off

echo *** Copying nix master visual-language.md to all skills ***
pause
for %%S in (kit lit pix dac dac-help cop wiz fix val act umm mem tut) do (
    if not exist ".\%%S\references" mkdir ".\%%S\references"
    robocopy ".\nix\references" ".\%%S\references" "visual-language.md" /COPY:DAT /DCOPY:E
)

echo *** Copying nix master documentation-standard.md to all skills (except pix) ***
for %%S in (kit lit cop wiz fix val tut) do (
    if not exist ".\%%S\references" mkdir ".\%%S\references"
    robocopy ".\nix\references" ".\%%S\references" "documentation-standard.md" /COPY:DAT /DCOPY:E
)

echo *** Copying jira-fields.local.yaml to agent roots ***
if exist ".\jira-fields.local.yaml" (
    copy /Y ".\jira-fields.local.yaml" "%USERPROFILE%\.claude\jira-fields.local.yaml"
    copy /Y ".\jira-fields.local.yaml" "%USERPROFILE%\.codex\jira-fields.local.yaml"
    copy /Y ".\jira-fields.local.yaml" "%USERPROFILE%\.agents\jira-fields.local.yaml"
)

echo *** Copying all skills to .claude, .codex, and .agent ***
pause
for %%S in (nix kit lit pix dac dac-help cop wiz fix val act umm mem tut) do (
    robocopy ".\%%S" "%USERPROFILE%\.claude\skills\%%S" /MIR /R:1 /W:1 /XJ
    robocopy ".\%%S" "%USERPROFILE%\.codex\skills\%%S" /MIR /R:1 /W:1 /XJ
    robocopy ".\%%S" "%USERPROFILE%\.agents\skills\%%S" /MIR /R:1 /W:1 /XJ
)

echo *** Done ***
pause
