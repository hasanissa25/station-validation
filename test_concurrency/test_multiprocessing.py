# flake8:noqa
from multiprocessing import Process, Queue


def make_calculation_one(queue, numbers):
    sample_result = f"Result from make calculation one {numbers}"
    if queue:
        queue.put({"Make_calculation_one": sample_result})


def main():
    queue = Queue()
    process_one = Process(target=make_calculation_one,
                          args=(queue, [1, 2, 3, 4],))
    process_one.start()
    process_one.join()
    results = queue.get()
    print(results["Make_calculation_one"])


if __name__ == '__main__':
    main()
