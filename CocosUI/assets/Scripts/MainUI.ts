import { _decorator, Component, Node } from 'cc';
const { ccclass, property } = _decorator;
import { Button , VideoPlayer} from "cc";
import { log, EventHandler } from 'cc';

@ccclass('MainUI')
export class MainUI extends Component {

    @property(Button)
    public playBtn:Button

    @property(VideoPlayer)
    public videoPlayer:VideoPlayer

    start() {

        this.count = 0
        const clickEventHandler = new EventHandler();
        clickEventHandler.target = this.node; // 这个 node 节点是你的事件处理代码组件所属的节点
        clickEventHandler.component = 'MainUI';// 这个是脚本类名
        clickEventHandler.handler = 'callback';
        clickEventHandler.customEventData = 'foobar';
        this.playBtn.clickEvents.push(clickEventHandler);
    }

    private count:number
    callback (event: Event, customEventData: string) {
        log("come btn")
        if(this.videoPlayer.isPlaying)
        {
            this.videoPlayer.pause()
        }
        else
        {
            if(this.count == 0)
            {
                this.videoPlayer.remoteURL = "https://rocbomb.oss-cn-beijing.aliyuncs.com/2002.mp4"
                this.count = 1
            }
            else
            {
                this.videoPlayer.remoteURL = "https://rocbomb.oss-cn-beijing.aliyuncs.com/2001.mp4"
                this.count = 0
            }
            this.videoPlayer.play()
        }
    }

    update(deltaTime: number) {
        
    }
}


