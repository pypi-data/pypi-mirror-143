import QtQuick

Window {
    title: 'PyPortable Installer'
    width: 400
    height: 320
    visible: true
    color: '#f2f2f2'

    Rectangle {
        anchors.centerIn: parent
        width: 200
        height: 200
        radius: 24
        color: '#ffffff'

        Text {
            anchors.centerIn: parent
            horizontalAlignment: Text.AlignHCenter
            color: '#333333'
//            font.bold: true
            text: 'Drag your project \nhere to start...'

            Behavior on color {
                ColorAnimation {
                    duration: 800
                }
            }

            Timer {
                interval: 2400
                running: true
                repeat: true

                property bool __flip: false

                onTriggered: {
                    this.__flip = !this.__flip
                    parent.color = this.__flip ? '#999999' : '#333333'
                }
            }
        }
    }
}
