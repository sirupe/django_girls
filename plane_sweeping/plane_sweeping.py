# 2. 모니터 클래스
class Monitor:
    # 2-1)생성시 모니터의 크기 정보(width, height) 를 받아 모니터를 생성한다.
    def __init__(self, positions):
        self.width = positions[0]
        self.height = positions[1]

    def is_bigger(self, process):
        if process.width > self.width:
            return True
        if process.height > self.height:
            return True
        return False


# 3. 프로세스 컨트롤러
class ProcessController:
    max_processing_count = 100

    # 3-1) 프로세스 컨트롤러 생성시 모니터 정보를 가지고 생성한다.
    def __init__(self, monitor):
        self.monitor = monitor
        # 실행중인 프로세스의 갯수를 생성시 0으로 초기화
        self.processing_count = 0
        # 실행중인 프로세스들 목록의 자료형을 set 으로 초기화
        self.processes = set()
        # 조각처리한 화면정보를 담은 목록의 자료형을 set 으로 초기화
        self.squares = set()

    # 4-2) 프로세스를 모니터에 띄운다.
    def open_process(self, process):
        # 조건 1) 열 수 있는 프로세스의 수는 이미 정해져 있음.
        if self.__is_opened_process_max__():
            raise OverflowError(f'프로세스를 더이상 열 수 없습니다. max:{self.max_processing_count}')
        # 조건 2) 모니터보다 큰 사이즈의 프로세스는 열 수 없음.
        if self.monitor.is_bigger(process):
            raise ValueError(f'프로세스 크기는 모니터 크기보다 작아야 합니다. monitor : w = {self.monitor.width}, h = {self.monitor.height}')

        # 열린 프로세스 목록에 프로세스를 추가한다.
        self.processes.add(process)
        # 열린 프로세스 갯수를 +1 한다.
        self.__increment_processing_count__()

    # 5-1) 생성된 프로세스들의 정보로 화면을 x축, y축 기준으로 분리된 직사각형들로 만들어 해당 정보를 저장한다.
    def make_squares(self):
        # 필요한 것은 중복되지 않는 x축의 꼭지점 좌표들과 y 축의 꼭지점 좌표들이므로 자료형은 set 으로 설정한다.
        xs = set()
        ys = set()
        # 프로세스들의 x, y 꼭지점 좌표들의 정보를 xs, ys 에 분할하여 저장한다.
        # 이유는 조각난 화면들의 정보는 열려있는 프로세스와 상관없이 각 분할된 구역의 크기를 계산할 목적으로 사용할 것이기 때문이다.
        for process in self.processes:
            xs.add(process.x1)
            xs.add(process.x2)
            ys.add(process.y1)
            ys.add(process.y2)
        # 모집한 xs 와 ys 를 작은 수 순으로 정렬한다.
        xs = sorted(xs)
        ys = sorted(ys)
        # 사각형은 4개의 꼭지점으로 만들어지고 4개의 꼭지점은 각각 x축의 위치 2개, y축의 위치 2개를 사용하므로 순서대로 x값 2개, y값 2개씩을 사용해가며 사각형들의 정보를 만들어 저장한다.
        for i in range(0, len(xs) - 1):
            x1 = xs[i]
            x2 = xs[i + 1]
            for j in range(0, len(ys) - 1):
                y1 = ys[j]
                y2 = ys[j + 1]
                self.squares.add(Square(x1, x2, y1, y2))

    # 6-1) 이미 구해진 프로세스와 사각형들로 점유중인 부분의 크기를 구한다.
    def get_total_occupied_area(self):
        # 반환값
        total_area = 0
        # 각 사각형들을 가지고
        for square in self.squares:
            print('square: ', square.x1, square.x2, square.y1, square.y2)
            # 열려있는 프로세스들에게 일일히 가지고 있는지 물어본다.
            for process in self.processes:
                print('process: ', process.x1, process.x2, process.y1, process.y2, process.has_square(square))
                # 가지고 있다면
                if process.has_square(square):
                    # 해당 사각형의 정보를 총 면적에 더한다.
                    total_area += square.area
                    # 중복된 값은 필요 없으므로 다음 프로세스에게는 물어보지 않아도 됨.
                    break

        return total_area

    def __is_opened_process_max__(self):
        return self.processing_count == self.max_processing_count

    def __increment_processing_count__(self):
        self.processing_count += 1



class Square:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.area = (x2 - x1) * (y2 - y1)


# 4. 화면에 떠 있는 하나의 창을 의미하는 프로세스
class Process:
    # 4-1) 생성시 프로세스의 위치정보를 받아 생성한다.
    def __init__(self, positions):
        # 입력값(위치정보)은 - 값이 들어올 수 없다.
        if [position for position in positions if position < 0]:
            raise ValueError('0보다 작은 크기의 process 는 생성할 수 없습니다.')

        # 위치정보를 의미에 맞게 해체한다.
        x = positions[0]
        y = positions[1]
        width = positions[2]
        height = positions[3]

        # 각 위치정보를 꼭지점과 상하, 좌우 의 길이로 계산하여 저장한다.
        self.x1 = x
        self.x2 = x + width
        self.y1 = y - height
        self.y2 = y
        self.width = width
        self.height = height

    # 6-1-1) 전달된 사각형이 이 프로세스 영역에 들어와 있는건지 구한다.
    def has_square(self, square):
        # 사각형의 x 시작과 끝이 프로세스 x 의 시작과 끝을 벗어난다면 가지고 있지 않은 것
        if square.x1 < self.x1 or square.x2 > self.x2:
            return False
        # 상동(y)
        if square.y1 < self.y1 or square.y2 > self.y2:
            return False

        return True


def main():
    print('start main')
    # 1. 인입되는 값은 모니터 사이즈(width, height), 실행될 창 갯수, 실행된 창의 갯수만큼의 위치정보(x, y, width, height)
    monitor_pixel = (100000000, 100000000)
    # 입력 조건에 있었지만 여기서 따로 사용하지는 않았다.
    processing_programs_count = 2
    programs_directions = [(0, 4, 6, 4), (3, 6, 5, 4)]
    # 2. 모니터 크기로 모니터 생성
    monitor = Monitor(monitor_pixel)
    # 3. 실행된 창(프로세스)들을 관리할 컨트롤러 생성
    process_controller = ProcessController(monitor)
    # 4. 프로세스의 위치정보의 갯수값을 바탕으로 프로세스들을 생성한다.
    for process in programs_directions:
        process_controller.open_process(Process(process))
    # 5. 프로세스의 x, y 값 기준으로 조각조각 난 분할된 화면정보들을 생성한다.
    process_controller.make_squares()
    # 6. 현재 열린 프로세스가 점유하고 있는 화면 크기 결과 출력.
    print(process_controller.get_total_occupied_area())


main()