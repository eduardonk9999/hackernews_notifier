@echo off
REM Script para agendar o bot no Agendador de Tarefas do Windows
REM Execute este script como Administrador

echo ========================================
echo Agendador do HackerNews Notifier
echo ========================================
echo.

REM Obtém o caminho completo do script Python
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%bot.py"
set "PYTHON_EXE=python"

REM Verifica se Python está instalado
where %PYTHON_EXE% >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERRO: Python nao encontrado!
    echo Certifique-se de que o Python esta no PATH.
    pause
    exit /b 1
)

echo Python encontrado!
echo Script: %PYTHON_SCRIPT%
echo.

REM Cria a tarefa agendada (executa diariamente às 18:00)
echo Criando tarefa agendada...
echo Executara diariamente as 18:00
echo.

schtasks /Create /TN "HackerNews Notifier" /TR "\"%PYTHON_EXE%\" \"%PYTHON_SCRIPT%\"" /SC DAILY /ST 18:00 /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo Tarefa criada com sucesso!
    echo ========================================
    echo.
    echo A tarefa "HackerNews Notifier" foi criada.
    echo Para editar: Abra o Agendador de Tarefas do Windows
    echo Para remover: schtasks /Delete /TN "HackerNews Notifier" /F
) else (
    echo.
    echo ========================================
    echo ERRO ao criar tarefa!
    echo ========================================
    echo.
    echo Tente executar este script como Administrador.
    echo Clique com botao direito e selecione "Executar como administrador"
)

echo.
pause

