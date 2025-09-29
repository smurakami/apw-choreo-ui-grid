from OSCSender import OSCSender
import asyncio
import numpy as np

async def main():
    """
    脳波送信のサンプルコードです。
    OSCSenderクラスに、データのフォーマット処理を記述しています。
    """
    sender = OSCSender(to_ip="192.168.1.80")

    async def bci_waveform_loop_01s():
        # counter = 0

        # 0.1秒ループ
        while True:
            # 脳波の生データの送信。24x30のfloat配列で送信します。
            length = np.random.randint(28, 35)
            # dummy_waveform = np.random.uniform(size=(24, 30))
            dummy_waveform = np.random.uniform(size=(24, length))

            # for i in range(dummy_waveform.shape[1]):
                # dummy_waveform[:, i] = counter % 1000
                # dummy_waveform[:, i] = counter % 1000
                # counter += 1

            sender.send_eeg(dummy_waveform)
            await asyncio.sleep(0.1)

    async def bci_label_loop_05s():
        # 0.5秒ループ
        while True:
            # 脳波の特徴量の送信。4000のfloat配列で送信します。（内部でチャンクに分割します。）
            dummy_eeg_feat = np.random.uniform(size=4000)
            sender.send_feat(dummy_eeg_feat)
            # 脳波の分類結果(確率)の送信。float型配列で送信します。
            dummy_label_prob = np.random.uniform(size=2)
            # dummy_label_prob = [0.1 + np.random.random() * 0.01, 0.9 -  np.random.random() * 0.01]
            sender.send_label_prob(dummy_label_prob)

            # 脳波の分類結果の送信。int型で送信します。
            dummy_label = np.argmax(dummy_label_prob)
            sender.send_label(dummy_label)
            await asyncio.sleep(0.5)


    # 両方のループを並列に実行
    await asyncio.gather(
        bci_waveform_loop_01s(),
        bci_label_loop_05s()
    )


if __name__ == "__main__":
    asyncio.run(main())
