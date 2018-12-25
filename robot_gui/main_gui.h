#ifndef MAIN_GUI_H
#define MAIN_GUI_H

#include <QMainWindow>

namespace Ui {
class main_gui;
}

class main_gui : public QMainWindow
{
    Q_OBJECT

public:
    explicit main_gui(QWidget *parent = 0);
    ~main_gui();

private:
    Ui::main_gui *ui;
};

#endif // MAIN_GUI_H
