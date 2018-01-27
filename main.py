import os
import hashlib
from tqdm import tqdm


HASH = {'4892bfc80d8e8343e5757d2f696ee14f8bd156fa5a544e88b20921bcd901a525': (1, 1),
        'a0977deaebde51a277b939b7ad1d814110616aaadaf0d0fc450459b09d147a3c': (1, 2),
        'd3609d9292918780b01acf5c8f1e3269d956ab3f7d295857a3b5ac369b8f85af': (1, 3),
        'd4032a78a25922b8527e3fc8932e33883fba788148e3f1b90aaad5a2a4c498cb': (1, 4),
        'f6c47ade00df02e45098bdfc887b25462860c6bb39ee4d8cc9edb97435983e1a': (1, 5),
        'ed90c6a00d2710f6c50ce849e6ac2db33085f8b2b06e79b575ac5edc813c1651': (1, 6),
        '3287bd23a8558285608c35a5ebbe877029ac85a7c6df41eaad30c2eeb06727c4': (1, 7),
        '5b98bc463a46c27211c78403ef7939b9a067e61e71f12eb24bf80eda7c17abc6': (1, 8),
        '47451df18a2b60e5265b2ff7a61480d2c919b6a4926e20e3f931a2cdb4ae6b2c': (2, 1),
        '0d7390588ac65637c1cd555a272db4b64d9aabdcc5495825e18ef7bb0932e200': (2, 2),
        '0d627399e2d2e40fbc9267bc047dd8c1a0dc0de30cdd6c85e7fd2f3f1f737f0c': (2, 3),
        '529255649f4e6313c2150310753f07d74cdd443d38c1f6a80da6fdcfa5c1b7d6': (2, 4),
        'dde7d905f9ff95a95664c3cfb4e006f2aa33f756f10d779dfd1aa168e0c6a170': (3, 1),
        '4afa5370696a039b1c486902894e0f00772ca95429be3a69998c7f37e31aa4c1': (3, 2),
        '0ff3deb79e49d7ebb0db51aed275295ba7a1e05728271b1c195570c558dab480': (3, 3),
        'f91d9355a208615463eb30e05455a5f21e1f91e7a888b7d806dee928b3d4abc3': (3, 4),
        '9ea06a4402bc5c275f285e69a1e7a692a0c751898842bdf9e91f227826a5f712': (3, 5)}


class DVDHash(object):
    def __init__(self, path):
        self.dir = path
        self.vobs = []
        self.exist = {1: [], 2: [], 3: []}

    def load_folder(self):
        for path, _, files in os.walk(self.dir):
            for file in files:
                if '.vob' in file.lower():
                    self.vobs.append([path, file])

    @staticmethod
    def calculate_hash(path, file):
        hash_256 = hashlib.sha256()
        print('\n다음 파일을 검사 중입니다: {}'.format(os.path.join(path, file)))
        file = os.path.join(path, file)
        with open(file, 'rb') as f:
            for chunk in tqdm(iter(lambda: f.read(1024*1024), b''), total=int(os.path.getsize(file)/1024/1024),
                              unit='MB'):
                hash_256.update(chunk)

        return hash_256.hexdigest()

    def process(self):
        self.load_folder()
        for path, file in self.vobs:
            hash_value = self.calculate_hash(path, file)
            try:
                disc, section = HASH[str(hash_value)]
                self.exist[disc].append(section)
            except KeyError:
                continue

        print('\n\n')
        for disc in self.exist:
            if disc == 1:
                full = list(range(1, 9))
            elif disc == 2:
                full = list(range(1, 5))
            elif disc == 3:
                full = list(range(1, 6))
            else:
                raise ValueError

            if len(self.exist[disc]) == 0:
                continue
            else:
                for section in sorted(self.exist[disc]):
                    print('다음 파일은 모두 정상입니다: {}번 디스크 {}번 파트'.format(disc, section))

            not_found = [x for x in full if x not in self.exist[disc]]
            if len(not_found) == 0:
                print('\n{}번 디스크 리핑 결과가 모두 정상입니다.'.format(disc))
            else:
                for section in not_found:
                    print(('\n다음 파일이 손상되었거나 찾을 수 없습니다. '
                           '{}번 디스크 {}번 파트 (VTS_0{}_{}.VOB 파일)').format(disc, section, disc, section))

            print('\n\n')


def main():
    print('=== 러블리즈 Alwayz DVD 리핑 무결성 테스트 --- 초코맛제티 ===\n\n')
    print(('검사 기준은 Moonrise°님의 결과(http://gall.dcinside.com/board/view/?id=lovelyz&no=3994178)를'
           ' 검증하여 참고하였습니다.\n\n'))
    target_folder = input('검사하려는 폴더 경로를 입력하거나 폴더를 창으로 끌어다 놓으십시오: ')
    hashs = DVDHash(target_folder.replace('"', ''))
    hashs.process()
    input('\n\n작업 완료.')


if __name__ == '__main__':
    main()
