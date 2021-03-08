# Crafting a gym-environment to simultate inventory managment
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>
# pylint: disable=no-self-use, attribute-defined-outside-init, protected-access

""" Test of abstract Task classes behavior """

import pytest
import pytest_check as check

from crafting.tasks.task import Task, TaskList

class TestTask:
    """ Task """

    def test_init(self):
        """ should instanciate correctly. """
        task = Task('task_name', 'world')
        check.equal(task.name, 'task_name')
        check.equal(task.world, 'world')

    def test_reward_raise(self):
        """ should raise Error if reward called without subclassing. """
        with pytest.raises(NotImplementedError):
            task = Task('task_name', 'world')
            task.reward('observation', 'previous_observation', 'action')

    def test_reward_done(self):
        """ should never be done by default. """
        task = Task('task_name', 'world')
        done = task.done('observation', 'previous_observation', 'action')
        check.is_false(done)

    def test_call(self, mocker):
        """ should call `done` and `reward` on call. """
        mocker.patch('crafting.tasks.task.Task.reward', lambda *args:1)
        mocker.patch('crafting.tasks.task.Task.done', lambda *args:True)
        task = Task('task_name', 'world')
        reward, done = task('observation', 'previous_observation', 'action')

        check.equal(reward, 1)
        check.is_true(done)


class TestTaskList:
    """ TaskList """

    @pytest.fixture(autouse=True)
    def setup(self):
        """ Setup dummy tasks """
        self.task_observe_123 = Task('obs_123', 'world')
        self.task_observe_123.reward = lambda obs, prev_obs, act: 2.1 * int(obs == '123')
        self.task_prev_observe_312 = Task('prev_obs_312', 'world')
        self.task_prev_observe_312.reward = lambda obs, prev_obs, act: 3.4 * int(prev_obs == '312')
        self.task_action_observe_213 = Task('action_213', 'world')
        self.task_action_observe_213.reward = lambda obs, prev_obs, act: 4.7 * int(act == '213')
        self.tasks = [
            self.task_observe_123,
            self.task_prev_observe_312,
            self.task_action_observe_213
        ]

    def test_init(self):
        """ should instanciate correctly. """
        TaskList(self.tasks)

    def test_init_raise_not_task(self):
        """ should raise TypeError if a task doesn't subclass crafting.Task. """
        tasks = [self.task_observe_123, 'task_str']
        with pytest.raises(TypeError, match=r".*must be.*crafting.Task.*"):
            TaskList(tasks)

    def test_call_none_task(self):
        """ should return (0, False) if tasks is None. """
        tasks = TaskList(None)
        reward, done = tasks('obs', 'prev_obs', 'action')
        check.equal(reward, 0)
        check.is_false(done)

    def test_call(self, mocker):
        """ should return accumulated rewards and done on call. """
        mocker.patch(
            'crafting.tasks.task.TaskList._get_task_weight',
            lambda *args: 1
        )
        mocker.patch(
            'crafting.tasks.task.TaskList._get_task_can_end',
            lambda *args: True
        )
        mocker.patch(
            'crafting.tasks.task.TaskList._stack_dones',
            lambda *args: True
        )
        tasks = TaskList(self.tasks)
        reward, done = tasks('123', '312', '213')
        check.equal(reward, 10.2)
        check.is_true(done)

class TestTaskListGetTaskWeight:
    """ TaskList._get_task_weight """

    def setup(self):
        """ Setup dummy tasks """
        self.task_observe_123 = Task('obs_123', 'world')
        self.task_prev_observe_312 = Task('prev_obs_312', 'world')
        self.task_action_observe_213 = Task('action_213', 'world')
        self.tasks = [
            self.task_observe_123,
            self.task_prev_observe_312,
            self.task_action_observe_213
        ]

    def test_list(self):
        """ should assign weights correctly if tasks_weights is a list."""
        self.tasklist = TaskList(self.tasks)

        expected_tasks_weights = [0.2, 0.1, 5]
        self.tasklist.tasks_weights = expected_tasks_weights

        tasks_weights = [
            self.tasklist._get_task_weight(task, i)
            for i, task in enumerate(self.tasklist.tasks)
        ]

        for value, expected in zip(tasks_weights, expected_tasks_weights):
            check.equal(value, expected)

    def test_dict(self):
        """ should assign weights correctly if tasks_weights is a dict."""
        self.tasklist = TaskList(self.tasks)

        expected_tasks_weights = {
            task.name: weight
            for task, weight in zip(self.tasks, [0.2, 0.1, 5])
        }
        self.tasklist.tasks_weights = expected_tasks_weights

        for i, task in enumerate(self.tasklist.tasks):
            value = self.tasklist._get_task_weight(task, i)
            expected = expected_tasks_weights[task.name]
            check.equal(value, expected)

    def test_none(self):
        """ should assign weights of 1 if tasks_weights is None."""
        self.tasklist = TaskList(self.tasks)
        for i, task in enumerate(self.tasklist.tasks):
            value = self.tasklist._get_task_weight(task, i)
            check.equal(value, 1)


class TestTaskListGetTaskCanEnd:
    """ TaskList._get_task_can_end """

    def setup(self):
        """ Setup dummy tasks """
        self.task_observe_123 = Task('obs_123', 'world')
        self.task_prev_observe_312 = Task('prev_obs_312', 'world')
        self.task_action_observe_213 = Task('action_213', 'world')
        self.tasks = [
            self.task_observe_123,
            self.task_prev_observe_312,
            self.task_action_observe_213
        ]

    def test_list(self):
        """ should assign `can_end` correctly if tasks_can_end is a list."""
        self.tasklist = TaskList(self.tasks)

        expected_tasks_can_end = [True, False, True]
        self.tasklist.tasks_can_end = expected_tasks_can_end

        tasks_weights = [
            self.tasklist._get_task_can_end(task, i)
            for i, task in enumerate(self.tasklist.tasks)
        ]

        for value, expected in zip(tasks_weights, expected_tasks_can_end):
            check.equal(value, expected)

    def test_dict(self):
        """ should assign `can_end` correctly if tasks_can_end is a dict."""
        self.tasklist = TaskList(self.tasks)

        expected_tasks_can_end = {
            task.name: can_end
            for task, can_end in zip(self.tasks, [True, False, True])
        }
        self.tasklist.tasks_can_end = expected_tasks_can_end

        for i, task in enumerate(self.tasklist.tasks):
            value = self.tasklist._get_task_can_end(task, i)
            expected = expected_tasks_can_end[task.name]
            check.equal(value, expected)

    def test_none(self):
        """ should assign True to all if tasks_can_end is None."""
        self.tasklist = TaskList(self.tasks)
        for i, task in enumerate(self.tasklist.tasks):
            value = self.tasklist._get_task_can_end(task, i)
            check.is_true(value)


class TestTaskListStackDones:
    """ TestList._stack_dones """

    def test_all(self):
        """ should return True only if all dones are True if early_stopping is 'all'. """
        tests = TaskList(None, early_stopping='all')

        dones = [True, False, True]
        done = tests._stack_dones(dones)
        check.is_false(done)

        dones = [True, True, True]
        done = tests._stack_dones(dones)
        check.is_true(done)

    def test_any(self):
        """ should return True if any dones is True if early_stopping is 'any'. """
        tests = TaskList(None, early_stopping='any')

        dones = [True, False, True]
        done = tests._stack_dones(dones)
        check.is_true(done)

        dones = [False, False, False]
        done = tests._stack_dones(dones)
        check.is_false(done)

    def test_raise_othervalue(self):
        """ should raise ValueError if early_stopping is not in ('any', 'all'). """
        tests = TaskList(None, early_stopping='x')
        dones = [True, False, True]
        with pytest.raises(ValueError, match=r"Unknown value for early_stopping.*"):
            tests._stack_dones(dones)
