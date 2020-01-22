from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QAbstractItemView, QScrollerProperties, QScroller


class TabDrink(QWidget):
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

    def populateList(self, drinkMenuList, tabCart):
        for drink in drinkMenuList:
            # Add to list a new item (item is simply an entry in your list)
            item = QListWidgetItem(self.mylist)

            # print(food.name)

            self.mylist.addItem(item)
            # Instantiate a custom widget
            drink.addToCartButton.clicked.connect(lambda checked, drink=drink: tabCart.addItem(drink))
            item.setSizeHint(drink.minimumSizeHint())

            # # Associate the custom widget to the list entry
            self.mylist.setItemWidget(item, drink)

    def clearList(self):
        self.mylist.clear()
