
import heapq
import threading


def schedule_jobs(w, jobs):
    ready = []
    workers = list(range(1, w + 1))
    heapq.heapify(workers)

    running = []
    results = []
    lock = threading.Lock()

    jobs.sort(key=lambda x: (x[0], x[1]))

    i = 0
    time = 0

    while i < len(jobs) or ready or running:

        # Complete jobs whose finish time has arrived
        while running and running[0][0] <= time:
            finish, worker, job = heapq.heappop(running)
            heapq.heappush(workers, worker)

        # Add all jobs that have arrived
        while i < len(jobs) and jobs[i][0] <= time:
            arrival, order, job_id, priority, duration, resources = jobs[i]

            with lock:
                heapq.heappush(
                    ready,
                    (-priority, arrival, order, job_id, duration, resources)
                )

            i += 1

        # Assign jobs to available workers
        while workers and ready:
            with lock:
                job = heapq.heappop(ready)

            priority, arrival, order, job_id, duration, resources = job

            worker = heapq.heappop(workers)
            start = time
            finish = start + duration

            results.append((job_id, worker, start, finish, arrival))

            heapq.heappush(running, (finish, worker, job_id))

        # Move time to the next event
        if running:
            next_finish = running[0][0]
        else:
            next_finish = float("inf")

        if i < len(jobs):
            next_arrival = jobs[i][0]
        else:
            next_arrival = float("inf")

        time = min(next_finish, next_arrival)

    # Print report in start-time order
    results.sort(key=lambda x: (x[2], x[1]))

    total_wait = 0

    for job_id, worker, start, finish, arrival in results:
        print(job_id, "W" + str(worker), start, finish)
        total_wait += start - arrival

    average = total_wait / len(results) if results else 0
    print("AVG_WAIT", format(average, ".2f"))


def main():
    w, n = map(int, input("Enter workers and number of jobs: ").split())

    jobs = []

    print("Enter arrival_time job_id priority duration resources:")

    for order in range(n):
        arrival, job_id, priority, duration, resources = input().split()

        jobs.append((
            int(arrival),
            order,
            job_id,
            int(priority),
            int(duration),
            int(resources)
        ))

    schedule_jobs(w, jobs)


if __name__ == "__main__":
    main()
