import asyncio
cache = {
    "clouds": None
}
# external_call_in_progress = False
external_call_in_progress_condition = None

async def get_clouds():
    global external_call_in_progress_condition
    global cache

    if cache["clouds"] is None:
        if external_call_in_progress_condition:
            print(f"ext_wait external_call_in_progress_condition, let's wait")
            async with external_call_in_progress_condition:
                await external_call_in_progress_condition.wait()
            print(f"ext_wait external_call_in_progress_condition, finished waiting")
        else:
            print(f"ext_create external_call_in_progress_condition not in progress, let's call")
            external_call_in_progress_condition = asyncio.Condition()
            clouds = await get_clouds_from_external_service()
            cache['clouds'] = clouds
            print(f"ext_create cache updated")
            async with external_call_in_progress_condition:
                external_call_in_progress_condition.notify_all()
            print(f"ext_create cache external_call_in_progress_condition notified")
            external_call_in_progress_condition = None
            print(f"ext_create external_call_in_progress_condition resed")
    else:
        print(f"ext_cache cache already exists")

    return cache['clouds']
    

# i want this value to be called only once i
# if it returnes 200 then we should cache it, following requests should receive value from cache.
# if it return 503 next calling client should call it again

external_service_call_count = 0

async def get_clouds_from_external_service():
    global external_service_call_count
    external_service_call_count += 1

    print(f'get_clouds_from_external_service')
    await asyncio.sleep(1)
    if external_service_call_count == 1:
        return None

    return [{"name": "aws"}, {"name": "gcp"}]

# When we request clouds and third party is down, we should return 503
# When third party is up again, we should return 200
# When multiple requests are made, we should call third party only once....

# @pytest.mark.asyncio
# async def test_caching():
#     tasks = [asyncio.create_task(get_clouds()) for i in range(5)]
#     _ = await asyncio.wait(tasks)

async def main():
    tasks_1 = [asyncio.create_task(get_clouds()) for i in range(5)]
    await asyncio.sleep(1)
    tasks_2 = [asyncio.create_task(get_clouds()) for i in range(5)]
    await asyncio.sleep(1)
    tasks_3 = [asyncio.create_task(get_clouds()) for i in range(5)]

    _ = await asyncio.wait(tasks_3)

    print([str(task.result()) for task in tasks_1])
    print([str(task.result()) for task in tasks_2])
    print([str(task.result()) for task in tasks_3])

asyncio.run(main())