from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QScrollerProperties, QScroller


class TabFood (QWidget):
    def __init__(self):
        super().__init__()

        self.hbox = QHBoxLayout()

        # Create the list
        self.mylist = QListWidget()
        self.mylist.setStyleSheet("QListWidget::item { border-bottom: 1px solid gray; }")
        self.mylist.setFocusPolicy(Qt.NoFocus)
        self.mylist.setSelectionMode(QAbstractItemView.NoSelection)
        self.mylist.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.mylist.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        self.sp = QScrollerProperties()
        self.sp.setScrollMetric(QScrollerProperties.DragVelocitySmoothingFactor, 0.6)
        self.sp.setScrollMetric(QScrollerProperties.MinimumVelocity, 0.0)
        self.sp.setScrollMetric(QScrollerProperties.MaximumVelocity, 0.2)
        self.sp.setScrollMetric(QScrollerProperties.AcceleratingFlickMaximumTime, 0.1)
        self.sp.setScrollMetric(QScrollerProperties.AcceleratingFlickSpeedupFactor, 1.2)
        self.sp.setScrollMetric(QScrollerProperties.SnapPositionRatio, 0.2)
        self.sp.setScrollMetric(QScrollerProperties.MaximumClickThroughVelocity, 1)
        self.sp.setScrollMetric(QScrollerProperties.DragStartDistance, 0.001)
        self.sp.setScrollMetric(QScrollerProperties.MousePressEventDelay, 0.5)

        self.scroller = QScroller.scroller(self.mylist.viewport())
        self.scroller.setScrollerProperties(self.sp)
        self.scroller.grabGesture(self.mylist.viewport(), QScroller.LeftMouseButtonGesture)

        self.mylist.show()
        self.hbox.addWidget(self.mylist)

        self.setLayout(self.hbox)

    def populateList(self, foodMenuList, tabCart):
        for food in foodMenuList:
            # Add to list a new item (item is simply an entry in your list)
            item = QListWidgetItem(self.mylist)

            # print(food.name)

            self.mylist.addItem(item)
            # Instanciate a custom widget
            food.addToCartButton.clicked.connect(lambda checked, food=food: tabCart.addItem(food))
            item.setSizeHint(food.minimumSizeHint())

            # # Associate the custom widget to the list entry
            self.mylist.setItemWidget(item, food)

    def clearList(self):
        self.mylist.clear()
