#include "main_gui.h"
#include "ui_main_gui.h"

main_gui::main_gui(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::main_gui)
{
    ui->setupUi(this);
}

main_gui::~main_gui()
{
    delete ui;
}
