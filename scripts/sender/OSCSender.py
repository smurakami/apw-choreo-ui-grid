from pythonosc import udp_client
import numpy as np
import numpy.typing as npt
import time

class OSCSender:
    def __init__(self, to_ip: str='127.0.0.1', to_port: int=12000):
        self.to_ip: str = to_ip
        self.to_port: int = to_port
        self.client = udp_client.SimpleUDPClient(to_ip, to_port)
        print(f"OSC Client initialized for {to_ip}:{to_port}")

    def send(self, address, value):
        """
        OSCメッセージを送信する
        :param address: OSCアドレス（例: "/example"）
        :param value: 送信する値（数値、文字列、リストなど）
        """
        try:
            self.client.send_message(address, value)
            # print(f"Sent: {address} {value}")
        except Exception as e:
            print(f"Failed to send message: {e}")

    # 脳波波形データ	/bci/eeg/[0-24]	float[30]	0.1s/signal
    # eeg: shape = (24, 30~)
    def send_eeg(self, eeg: npt.NDArray):
        timestamp = int(time.time() * 1000)
        for index, waveform in enumerate(eeg):
            value = list(map(float, waveform))
            address = f"/bci/eeg/{index:02d}"
            self.send(address, [timestamp, *value])

    # 脳波中間特徴	/bci/feat	float[4000]	0.5s/signal
    # feat: shape = (4000,)
    def send_feat(self, feat: npt.NDArray):
        timestamp = int(time.time() * 1000)
        chunk_size = 1000
        chunks = feat.reshape((-1, chunk_size))
        for index, chunk in enumerate(chunks):
            value = list(map(float, chunk))
            address = f"/bci/feat/{index:02d}"
            self.send(address, [timestamp, *value])

    # 脳波分類結果	/bci/label	int	0.5s/signal
    # label: int
    def send_label(self, label: int):
        timestamp = int(time.time() * 1000)
        value = int(label)
        address = f"/bci/label"
        self.send(address, [timestamp, value])

    # 脳波分類結果	/bci/label_prob float[2]	0.5s/signal
    # probs: shape =  (2,)
    def send_label_prob(self, probs: npt.NDArray):
        timestamp = int(time.time() * 1000)
        value = list(map(float, probs))
        address = f"/bci/label_prob"
        self.send(address, [timestamp, *value])
