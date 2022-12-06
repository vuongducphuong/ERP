odoo.define('sale_ex.giam_gia_hang_ban_form_view', function (require) {
    "use strict";

    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var view_registry = require('web.view_registry');

    var GiamGiaHangBanController = FormController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            
            if (this.getFieldValue('selection_chung_tu_giam_gia_hang_ban') == 'giam_tru_cong_no'){
                blackList['02-TT: Phiếu chi'] = true;
                blackList['02-TT:Phiếu chi (Mẫu A5)'] = true;
                blackList['02-TT:Phiếu chi (Mẫu 2 liên)'] = true;

            }
            return blackList;
        },
        onFieldChanged: function(field){
            var self = this;
            if(field == 'CHUNG_TU_BAN_HANG'){
                var CHUNG_TU_BAN_HANG = this.getFieldValue('CHUNG_TU_BAN_HANG')
                var id_ctbh;
                var name_ctbh;
                if (CHUNG_TU_BAN_HANG){
                    id_ctbh =  CHUNG_TU_BAN_HANG.id;
                    name_ctbh = CHUNG_TU_BAN_HANG.display_name;
                }
                this.rpc_action({
                    model: 'sale.ex.giam.gia.hang.ban',
                    method: 'lay_du_lieu_chung_tu_ban_hang',
                    args: {
                        'chung_tu_ban_hang_id' :id_ctbh,
                        'chung_tu_ban_hang_name' : name_ctbh,
                    },
                    callback: function(result) {
                        if (result) {
                            self.updateUI(result);
                        }
                    }
                });
            }
        }
    });
    
    var GiamGiaHangBanView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: GiamGiaHangBanController,
        }),
    });
    
    view_registry.add('giam_gia_hang_ban_form_view', GiamGiaHangBanView);
    
    return GiamGiaHangBanView;
});

odoo.define('sale_ex.giam_gia_hang_ban_list_view', function (require) {
    "use strict";

    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    var view_registry = require('web.view_registry');

    var GiamGiaHangBanController = ListController.extend({
        getPrintBlackList:function () {
            var blackList = {};
            var selectedRecords = this.getSelectedRecords();
            for (var i=0; i<selectedRecords.length; i++) {
                var record = selectedRecords[i].data;
                if (record.selection_chung_tu_giam_gia_hang_ban == 'giam_tru_cong_no'){
                    blackList['02-TT: Phiếu chi'] = true;
                    blackList['02-TT:Phiếu chi (Mẫu A5)'] = true;
                    blackList['02-TT:Phiếu chi (Mẫu 2 liên)'] = true;
    
                }
            }
            return blackList;
        },
    });
    
    var GiamGiaHangBanView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: GiamGiaHangBanController,
        }),
    });
    
    view_registry.add('giam_gia_hang_ban_list_view', GiamGiaHangBanView);
    
    return GiamGiaHangBanView;
});