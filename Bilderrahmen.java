import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
/** Erzeuge ein Swing-Fenster mit einem Menue, einer
    Toolbar und einem Label mit Iconimage */
public class Bilderrahmen extends JFrame {
  Container c;           // Container dieses Frames
  JMenuBar menuBar;      // Menueleiste
  JMenu menu;            // Menue
  JMenuItem menuItem;    // Menue-Eintrag
  JToolBar toolBar;      // Werkzeugleiste
  JButton button;        // Knoepfe der Werkzeugleiste
  JLabel bildLabel;      // Label, das im Frame erscheinen soll
  
  public Bilderrahmen() {  // Konstruktor
    // Bestimme die Referenz auf den eigenen Container
    c = getContentPane();
    
    // Erzeuge das Listener-Objekt fuer das Menue
    MenuListener mL = new MenuListener();
    
    // Erzeuge die Menueleiste
    menuBar = new JMenuBar();

    // Erzeuge ein Menue
    menu = new JMenu("Bilder");
    menu.setMnemonic(KeyEvent.VK_B);

    // Erzeuge die Menue-Eintraege und fuege sie dem Menue hinzu
    menuItem = new JMenuItem("Hund");
    menuItem.setMnemonic(KeyEvent.VK_H);
    menuItem.addActionListener(mL);    // Fuege den Listener hinzu
    menuItem.setActionCommand("dog");  // Setze die Aktionsbezeichnung
    menu.add(menuItem);
    menuItem = new JMenuItem("Katze");
    menuItem.setMnemonic(KeyEvent.VK_K);
    menuItem.addActionListener(mL);    // Fuege den Listener hinzu
    menuItem.setActionCommand("cat");  // Setze die Aktionsbezeichnung
    menu.add(menuItem);
    menuItem = new JMenuItem("Maus");
    menuItem.setMnemonic(KeyEvent.VK_M);
    menuItem.addActionListener(mL);    // Fuege den Listener hinzu
    menuItem.setActionCommand("mouse");// Setze die Aktionsbezeichnung
    menu.add(menuItem);

    // Fuege das Menue der Menueleiste hinzu
    menuBar.add(menu);

    // Fuege die Menueleiste dem Frame hinzu
    setJMenuBar(menuBar);

    // Erzeuge das Listener-Objekt fuer die Werkzeugleiste
    ToolBarListener tL = new ToolBarListener();

    // Erzeuge die Werkzeugleiste
    toolBar = new JToolBar("Rahmenfarbe");
    // Erzeuge die Knoepfe
    button = new JButton(new ImageIcon("images/rot.gif"));
    button.setToolTipText("roter Rahmen");
    button.addActionListener(tL);       // Fuege den Listener hinzu 
    button.setActionCommand("rot");     // Setze die Aktionsbezeichnung
    toolBar.add(button);
    button = new JButton(new ImageIcon("images/gruen.gif"));
    button.setToolTipText("gruener Rahmen");
    button.addActionListener(tL);       // Fuege den Listener hinzu
    button.setActionCommand("gruen");   // Setze die Aktionsbezeichnung
    toolBar.add(button);
    button = new JButton(new ImageIcon("images/blau.gif"));
    button.setToolTipText("blauer Rahmen");
    button.addActionListener(tL);       // Fuege den Listener hinzu
    button.setActionCommand("blau");    // Setze die Aktionsbezeichnung
    toolBar.add(button);
    
    // Erzeuge das Label mit Initial-Bild
    bildLabel = new JLabel(new ImageIcon("images/dog.gif"));
    
    // Setze die Initial-Hintergrundfarbe des Bilderrahmens und 
    // fuege das Label und die Toolbar dem Container hinzu
    c.setBackground(Color.RED);
    c.add(bildLabel, BorderLayout.CENTER);
    c.add(toolBar, BorderLayout.NORTH);
  }
  
  // Innere Listener-Klasse fuer das Menue
  class MenuListener implements ActionListener {
    public void actionPerformed(ActionEvent e) {
      // Bildauswahl abhaengig von der Aktionsbezeichnung aendern
      bildLabel.setIcon(new ImageIcon("images/"
                                      + e.getActionCommand() 
                                      + ".gif"));
    }
  }
  
  // Innere Listener-Klasse fuer die Toolbar
  class ToolBarListener implements ActionListener {
    public void actionPerformed(ActionEvent e) {
      // Hintergrundfarbe abhaengig von der Aktionsbezeichnung aendern
      if (e.getActionCommand() == "rot")
        c.setBackground(Color.RED);
      else if (e.getActionCommand() == "gruen")
        c.setBackground(Color.GREEN);
      else if (e.getActionCommand() == "blau")
        c.setBackground(Color.BLUE);
    }
  }
  
  public static void main(String[] args) {
     Bilderrahmen fenster = new Bilderrahmen();
     fenster.setTitle("Bilderrahmen");
     fenster.setSize(180,280);
     fenster.setVisible(true);
     fenster.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
  }
}
