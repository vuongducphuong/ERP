odoo.define('ketoan.ketoan_bao_cao_quy_tien_mat', function (require) {
    'use strict';
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var rpc = require('web.rpc');
    var session = require('web.session');
    var utils = require('web.utils');
    var QWeb = core.qweb;
    var _t = core._t;
    var framework = require('web.framework');

    var datepicker = require('web.datepicker');
    var time = require('web.time');

    window.click_num = 0;
    var SoQuyTienMat = AbstractAction.extend({
    template: 'QuyTienMatTemp',
        events: {
            'click .parent-line': 'journal_line_click',
            'click .child_col1': 'journal_line_click',
            'click #apply_filter': 'apply_filter',
            'click #pdf': 'print_pdf',
            'click #xlsx': 'print_xlsx',
            'click .gl-line': 'show_drop_down',
            'click .view-account-move': 'view_acc_move',
            'mousedown div.input-group.date[data-target-input="nearest"]': '_onCalendarIconClick',
        },

        init: function(parent, action) {
        this._super(parent, action);
                this.currency=action.currency;
                this.report_lines = action.report_lines;
                this.wizard_id = action.context.wizard | null;
            },


        start: function() {
            var self = this;
            self.initial_render = true;
            if (this.searchModel.config.domain.length != 0) {
                rpc.query({
                    model: 'ketoan.bao.cao.quy.tien.mat',
                    method: 'create',
                    args: [{
                         account_ids : [this.searchModel.config.domain[0][2]]
                    }]
                }).then(function(t_res) {
                    self.wizard_id = t_res;
                    self.load_data(self.initial_render);
                })
            }else{
            rpc.query({
                    model: 'ketoan.bao.cao.quy.tien.mat',
                    method: 'create',
                    args: [{

                    }]
                }).then(function(t_res) {
                    self.wizard_id = t_res;
                    self.load_data(self.initial_render);
                })
            }
        },


        _onCalendarIconClick: function (ev) {
            var $calendarInputGroup = $(ev.currentTarget);

            var calendarOptions = {

            minDate: moment({ y: 1000 }),
                maxDate: moment().add(200, 'y'),
                calendarWeeks: true,
                defaultDate: moment().format(),
                sideBySide: true,
                buttons: {
                    showClear: true,
                    showClose: true,
                    showToday: true,
                },

                icons : {
                    date: 'fa fa-calendar',

                },
                locale : moment.locale(),
                format : time.getLangDateFormat(),
                 widgetParent: 'body',
                 allowInputToggle: true,
            };

            $calendarInputGroup.datetimepicker(calendarOptions);
        },


        load_data: function (initial_render = true) {
            var self = this;
                self.$(".categ").empty();
                try{
                    var self = this;
                    var action_title = self._title
                    self._rpc({
                        model: 'ketoan.bao.cao.quy.tien.mat',
                        method: 'view_report',
                        args: [[this.wizard_id], action_title],
                    }).then(function(datas) {

                            if (initial_render) {
                                    self.$('.filter_view_tb').html(QWeb.render('QuyTienMatTimKiemView', {
                                        filter_data: datas['filters'],
                                        title : datas['name'],
                                    }));
                                    self.$el.find('.account').select2({
                                        placeholder: ' Lo???i...',
                                    });
                                    self.$el.find('.target_move').select2({
                                        placeholder: 'T??nh tr???ng...',
                                    });

                            }
                            var child=[];
                        self.$('.table_view_tb').html(QWeb.render('QuyTienMatBangKetQuaView', {

                                            report_lines : datas['report_lines'],
                                            filter : datas['filters'],
                                            currency : datas['currency'],
                                            credit_total : datas['credit_total'],
                                            debit_total : datas['debit_total'],
                                            debit_balance : datas['debit_balance']
                                        }));

                });

                    }
                catch (el) {
                    window.location.href
                    }
            },

            print_pdf: function(e) {
            e.preventDefault();
            var self = this;
            var action_title = self._title
            self._rpc({
                model: 'ketoan.bao.cao.quy.tien.mat',
                method: 'view_report',
                args: [
                    [self.wizard_id], action_title
                ],
            }).then(function(data) {
                var action = {
                    'type': 'ir.actions.report',
                    'report_type': 'qweb-pdf',
                    'report_name': 'ketoan.bao_cao_so_cai',
                    'report_file': 'ketoan.bao_cao_so_cai',
                    'data': {
                        'report_data': data
                    },
                    'context': {
                        'active_model': 'ketoan.bao.cao.quy.tien.mat',
                        'landscape': 1,
                        'trial_pdf_report': true
                    },
                    'display_name': action_title,
                };
                return self.do_action(action);
            });
        },

        print_xlsx: function() {
            var self = this;
            var action_title = self._title
            self._rpc({
                model: 'ketoan.bao.cao.quy.tien.mat',
                method: 'view_report',
                args: [
                    [self.wizard_id], action_title
                ],
            }).then(function(data) {
                var action = {
//                    'type': 'ir_actions_dynamic_xlsx_download',
                    'data': {
                         'model': 'ketoan.bao.cao.quy.tien.mat',
                         'options': JSON.stringify(data['filters']),
                         'output_format': 'xlsx',
                         'report_data': JSON.stringify(data['report_lines']),
                         'report_name': action_title,
                         'dfr_data': JSON.stringify(data),
                    },
                };
//                return self.do_action(action);
                self.downloadXlsx(action)
            });
        },

        downloadXlsx: function (action){
            framework.blockUI();
                session.get_file({
                    url: '/dynamic_xlsx_reports',
                    data: action.data,
                    complete: framework.unblockUI,
                    error: (error) => this.call('crash_manager', 'rpc_error', error),
                });
            },



        create_lines_with_style: function(rec, attr, datas) {
            var temp_str = "";
            var style_name = "border-bottom: 1px solid #e6e6e6;";
            var attr_name = attr + " style="+style_name;

            temp_str += "<td  class='child_col1' "+attr_name+" >"+rec['code'] +rec['name'] +"</td>";
            if(datas.currency[1]=='after'){
            temp_str += "<td  class='child_col2' "+attr_name+" >"+rec['debit'].toFixed(2)+datas.currency[0]+"</td>";
            temp_str += "<td  class='child_col3' "+attr_name+" >"+rec['credit'].toFixed(2) +datas.currency[0]+ "</td>";
            }
            else{
            temp_str += "<td  class='child_col2' "+attr_name+" >"+datas.currency[0]+rec['debit'].toFixed(2) + "</td>";
            temp_str += "<td  class='child_col3' "+attr_name+">"+datas.currency[0]+rec['credit'].toFixed(2) + "</td>";

            }
            return temp_str;
        },


        journal_line_click: function (el){
            click_num++;
            var self = this;
            var line = $(el.target).parent().data('id');
            return self.do_action({
                type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: 'account.move',
                    views: [
                        [false, 'form']
                    ],
                    res_id: line,
                    target: 'current',
            });

        },
        format_currency: function(currency, amount) {
                if (typeof(amount) != 'number') {
                    amount = parseFloat(amount);
                }
                var formatted_value = (parseInt(amount)).toLocaleString(currency[2],{
                    minimumFractionDigits: 2
                })
                return formatted_value
            },

        show_drop_down: function(event) {
            event.preventDefault();
            var self = this;
            var account_id = $(event.currentTarget).data('account-id');
            var offset = 0;
            var td = $(event.currentTarget).next('tr').find('td');
            if (td.length == 1) {
                    var action_title = self._title
                    self._rpc({
                        model: 'ketoan.bao.cao.quy.tien.mat',
                        method: 'get_accounts_line',
                        args: [
                            [self.wizard_id], account_id, action_title
                        ],
                    }).then(function(data) {

                    for (var i = 0; i < data['report_lines'].length; i++) {

                    if (account_id == data['report_lines'][i]['id'] ){
                    $(event.currentTarget).next('tr').find('td').remove();
                    $(event.currentTarget).next('tr').after(
                        QWeb.render('QuyTienMatChiTietView', {
                            account_data: data['report_lines'][i]['move_lines'],
                            currency_symbol : data.currency[0],
                            id : data['report_lines'][i]['id'],
                            currency_position : data.currency[1],

                        }))
                    $(event.currentTarget).next('tr').find('td ul li:first a').css({
                        'background-color': '#00ede8',
                        'font-weight': 'bold',
                    });
                     }
                    }

                    });
            }
        },

        view_acc_move: function(event) {
            event.preventDefault();
            var self = this;
            var context = {};
            var show_acc_move = function(res_model, res_id, view_id) {
                var action = {
                    type: 'ir.actions.act_window',
                    view_type: 'form',
                    view_mode: 'form',
                    res_model: res_model,
                    views: [
                        [view_id || false, 'form']
                    ],
                    res_id: res_id,
                    target: 'current',
                    context: context,
                };
                return self.do_action(action);
            };
            rpc.query({
                    model: 'account.move',
                    method: 'search_read',
                    domain: [
                        ['id', '=', $(event.currentTarget).data('move-id')]
                    ],
                    fields: ['id'],
                    limit: 1,
                })
                .then(function(record) {
                    if (record.length > 0) {
                        show_acc_move('account.move', record[0].id);
                    } else {
                        show_acc_move('account.move', $(event.currentTarget).data('move-id'));
                    }
                });
        },

        apply_filter: function(event) {

            event.preventDefault();
            var self = this;
            self.initial_render = false;

            var filter_data_selected = {};


            var account_ids = [];
            var account_text = [];

            var account_res = document.getElementById("acc_res")
            var account_list = $(".account").select2('data')
            for (var i = 0; i < account_list.length; i++) {
                if(account_list[i].element[0].selected === true){

                    account_ids.push(parseInt(account_list[i].id))
                    if(account_text.includes(account_list[i].text) === false){
                        account_text.push(account_list[i].text)
                    }
                    account_res.value = account_text
                    account_res.innerHTML=account_res.value;
                }
            }
            if (account_list.length == 0){
               account_res.value = ""
                    account_res.innerHTML="";

            }
            filter_data_selected.account_ids = account_ids


 if (this.$el.find('.datetimepicker-input[name="gen_date_from"]').val()) {
                filter_data_selected.date_from = moment(this.$el.find('.datetimepicker-input[name="gen_date_from"]').val(), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            }

            if (this.$el.find('.datetimepicker-input[name="gen_date_to"]').val()) {
                filter_data_selected.date_to = moment(this.$el.find('.datetimepicker-input[name="gen_date_to"]').val(), time.getLangDateFormat()).locale('en').format('YYYY-MM-DD');
            }

            if ($(".target_move").length) {
            var post_res = document.getElementById("post_res")
            filter_data_selected.target_move = $(".target_move")[1].value
            post_res.value = $(".target_move")[1].value
                    post_res.innerHTML=post_res.value;
              if ($(".target_move")[1].value == "") {
              post_res.innerHTML="posted";

              }
            }
            rpc.query({
                model: 'ketoan.bao.cao.quy.tien.mat',
                method: 'write',
                args: [
                    self.wizard_id, filter_data_selected
                ],
            }).then(function(res) {
            self.initial_render = false;
                self.load_data(self.initial_render);
            });
        },

    });
    core.action_registry.add("quy_tien_mat", SoQuyTienMat);
    return SoQuyTienMat;
});