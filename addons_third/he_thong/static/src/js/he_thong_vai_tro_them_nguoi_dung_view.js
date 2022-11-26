odoo.define('he_thong.vai_tro_them_nguoi_dung_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var VaiTroNguoiDungController = FormController.extend({
        init: function () {
            this._super.apply(this, arguments);
        },

        _onButtonClicked: function(event) {
            var self = this;
			event.stopPropagation();
            switch (event.data.attrs.name)
            {
                case "action_save":
                    var dxHandler = this.getFieldWidget('CHI_TIET_IDS').dxHandler;
                    var vai_tro = this.getFieldValue('VAI_TRO_ID');
                    var selectedList = dxHandler.getSelectedRowKeys("all");
                    var dataSource = dxHandler.option('dataSource');
                    var selected = [];
                    for (var i=0; i<selectedList.length; i++) {
                        var selectedRow = _.find(dataSource, function(el) {
                            return el.menu == selectedList[i];
                        })
                        if (selectedRow && selectedRow.permission_id) {
                            selected.push({
                                VAI_TRO_ID: vai_tro.id,
                                menu_id: selectedRow.parent_menu_id && selectedRow.parent_menu_id.res_id,
                                report_id: selectedRow.parent_report_id && selectedRow.parent_report_id.res_id,
                                permission_id: selectedRow.permission_id.res_id,
                            });
                        }
                    }
                    this.rpc_action({
                        model: 'he.thong.vai.tro.nguoi.dung',
                        method: 'action_save',
                        args: {
                           selected: selected,
                        },
                        callback: function() {
                            self.do_action({type: 'ir.actions.act_window_close'});
                        }
                    });
                    break;
                    
                default: 
                   this._super.apply(this, arguments);
            }
            
        }
    });
    
    var VaiTroNguoiDungView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: VaiTroNguoiDungController,
        }),
    });
    
    view_registry.add('vai_tro_them_nguoi_dung_view', VaiTroNguoiDungView);
    
    return VaiTroNguoiDungView;
});
