odoo.define('phan_tich.phan_tich_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');
    var data_manager = require('web.data_manager');

    var PhanTichController = ListController.extend({
        onOpenRecord: function(event) {
            var self = this;
            var rowData = this.model.localData[event.data.id];
            // var res_model = rowData.data.RES_MODEL;
            // var view_id = rowData.data.VIEW_ID;
            var action_id = rowData.data.ACTION_ID;
            if (action_id) {
                return data_manager.load_action(action_id).then(function(result) {
                    return self.do_action(result);
            });;
            }
            // if (res_model && view_id) {
            //     return new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
            //         res_model: res_model,
            //         title: 'Chọn tham số...',
            //         view_id: view_id,
            //         size: rowData.data.form_size || 'large',
            //     })).open();
            // }
        },
       
    });
    
    var PhanTichView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: PhanTichController,
        }),
    });
    
    view_registry.add('phan_tich_list_view', PhanTichView);
    
    return PhanTichView;
});
