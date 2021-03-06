#!/usr/bin/env python
#
# tests controllers/clouds/gui.py
#
# Copyright 2016 Canonical, Ltd.


import unittest
from unittest.mock import MagicMock, call, patch

from conjureup.controllers.juju.clouds.gui import CloudsController


class CloudsGUIRenderTestCase(unittest.TestCase):

    def setUp(self):
        self.controller = CloudsController()

        self.finish_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.CloudsController.finish')
        self.mock_finish = self.finish_patcher.start()

        self.view_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.CloudView')
        self.view_patcher.start()
        self.app_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.app')
        mock_app = self.app_patcher.start()
        mock_app.ui = MagicMock(name="app.ui")
        self.list_clouds_patcher = patch(
            'conjureup.juju.get_compatible_clouds')
        self.mock_list_clouds = self.list_clouds_patcher.start()
        self.mock_list_clouds.return_value = ['test1', 'test2']
        self.get_clouds_patcher = patch(
            'conjureup.juju.get_clouds')
        self.mock_get_clouds_patcher = self.get_clouds_patcher.start()

    def tearDown(self):
        self.finish_patcher.stop()
        self.view_patcher.stop()
        self.app_patcher.stop()
        self.list_clouds_patcher.stop()
        self.get_clouds_patcher.stop()

    def test_render(self):
        "call render"
        self.controller.render()


class CloudsGUIFinishTestCase(unittest.TestCase):

    def setUp(self):
        self.controller = CloudsController()

        self.controllers_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.controllers')
        self.mock_controllers = self.controllers_patcher.start()
        self.utils_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.utils')
        self.mock_utils = self.utils_patcher.start()

        self.render_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.CloudsController.render')
        self.mock_render = self.render_patcher.start()
        self.app_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.app')
        self.mock_app = self.app_patcher.start()
        self.mock_app.ui = MagicMock(name="app.ui")

        self.cloud_types_patcher = patch(
            'conjureup.juju.get_cloud_types_by_name')
        self.mock_cloud_types = self.cloud_types_patcher.start()
        self.mock_cloud_types.return_value = {'aws': 'ec2'}

        self.cloudname = 'testcloudname'

        self.track_event_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.track_event')
        self.mock_track_event = self.track_event_patcher.start()

        self.mock_provider = MagicMock()
        self.load_schema_patcher = patch(
            'conjureup.controllers.juju.clouds.gui.load_schema',
            self.mock_provider)
        self.mock_load_schema = self.load_schema_patcher.start()

    def tearDown(self):
        self.controllers_patcher.stop()
        self.render_patcher.stop()
        self.app_patcher.stop()
        self.track_event_patcher.stop()
        self.utils_patcher.stop()
        self.load_schema_patcher.stop()

    def test_finish_no_controller(self):
        "clouds.finish without existing controller"
        self.mock_utils.gen_model.renturn_type = 'abacadaba'
        self.controller.finish('aws')
        self.mock_controllers.use.assert_has_calls([
            call('credentials'), call().render()])
