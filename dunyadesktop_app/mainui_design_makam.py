from PyQt5.QtWidgets import QWidget

from general_design import GeneralMainDesign


class MainWindowMakamDesign(GeneralMainDesign):
    """The main window design of makam culture.
    Inherits GeneralMainDesign and changes the names of the labels."""
    def __init__(self):
        # setting the interface
        GeneralMainDesign.__init__(self)

        self._set_main_label()
        self._set_score_tab()
        self._retranslate_ui_elements()

    def _set_main_label(self):
        """Changes the text of the label """
        self.dwc_top.label_corpus.setText('<html><head/><body><p '
                                          'align="center"><span style=" '
                                          'font-size:15pt; '
                                          'color:#C1C1C1;">Ottoman-Turkish '
                                          'Makam Music '
                                          'Corpus</span></p></body></html>')

    def _set_score_tab(self):
        """Adds a score tab for score collection"""
        self.tab_score = QWidget(self)
        self.frame_query.tabWidget.addTab(self.tab_score, "")

    def _retranslate_ui_elements(self):
        """Changes the names of comboboxes and tabs"""
        self.frame_query.tabWidget.setTabText(
            self.frame_query.tabWidget.indexOf(self.tab_score),
            "Score Collection")

        self.frame_query.frame_attributes.comboBox_melodic.\
            set_placeholder_text('Makam')
        self.frame_query.frame_attributes.comboBox_form.\
            set_placeholder_text('Form')
        self.frame_query.frame_attributes.comboBox_rhythm.\
            set_placeholder_text('Usul')
