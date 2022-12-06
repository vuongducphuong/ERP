odoo.define('tien_ich.bao_cao_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');
    var dialogs = require('web.view_dialogs');

    var BaoCaoController = ListController.extend({
        onOpenRecord: function(event) {
            var rowData = this.model.localData[event.data.id];
            var res_model = rowData.data.RES_MODEL;
            var view_id = rowData.data.VIEW_ID;
            if (res_model && view_id) {
                return new dialogs.FormParamsDialog(this, _.extend({}, this.nodeOptions, {
                    res_model: res_model,
                    title: 'Chọn tham số...',
                    view_id: view_id,
                    size: rowData.data.form_size || 'large',
                })).open();
            }
        },
       
    });
    
    var BaoCaoView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: BaoCaoController,
        }),
    });
    
    view_registry.add('bao_cao_list_view', BaoCaoView);
    
    return BaoCaoView;
});
