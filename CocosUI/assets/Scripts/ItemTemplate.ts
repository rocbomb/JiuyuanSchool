import { _decorator, Component, Node, Label, Sprite} from 'cc';
import { VideoItem } from './VideoList';
const { ccclass, property } = _decorator;

@ccclass('ItemTemplate')
export class ItemTemplate extends Component {
    @property
    public id = 0;
    @property(Label)
    public itemName: Label | null = null;
    @property(Label)
    public itemTime: Label | null = null;
    @property(Sprite)
    public OkImage: Sprite | null = null;

    init(data: VideoItem) {
        this.id = data.id;
        this.OkImage.enabled = data.isOk;
        this.itemName.string = data.itemName;
        this.itemTime.string = data.itemTime + "分钟";
    }
}


