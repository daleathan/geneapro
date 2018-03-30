import * as React from 'react';
import { connect } from 'react-redux';
import 'fixed-data-table/dist/fixed-data-table.css';
import Page from './Page';
import { AppState, GPDispatch } from './Store/State';
import { Input, Segment } from 'semantic-ui-react';
import { Person, PersonSet } from './Store/Person';
import { GenealogyEventSet } from './Store/Event';
import { PersonaLink } from './Links';
import { Table, CellProps, Column, Cell } from 'fixed-data-table';
import { extractYear } from './Store/Event';
import { fetchPersons } from './Store/Sagas';

import './PersonaList.css';

interface PersonaListProps {
   persons: PersonSet;
   allEvents: GenealogyEventSet;
   dispatch: GPDispatch;
}

interface PersonaListState {
   filter?: string;
   persons: Person[];  // sorted
}

class PersonaListConnected extends React.PureComponent<PersonaListProps, PersonaListState> {
   constructor() {
      super();
      this.state = {
         filter: '',
         persons: [],
      };
   }

   componentWillReceiveProps(nextProps: PersonaListProps) {
      if (nextProps.persons !== this.props.persons) {
         this.setState((s: PersonaListState) => ({
            ...s,
            persons: this.computePersons(nextProps.persons, s.filter),
         }));
      }
   }

   componentWillMount() {
      this.props.dispatch(fetchPersons.request({}));
   }

   computePersons(set: PersonSet, filter?: string): Person[] {
      let list = Object.values(set)
         .sort((p1, p2) => p1.name.localeCompare(p2.name));

      if (filter) {
         list = list.filter(
            (p: Person) => p.name.toLowerCase().indexOf(filter) >= 0
         );
      }

      return list;
   }

   filterChange = (e: React.FormEvent<HTMLElement>, val: {value: string}) => {
      this.setState({
         filter: val.value,
         persons: this.computePersons(this.props.persons, val.value),
      });
   }

   render() {
      const width = 900;
      document.title = 'List of persons';

      const idWidth = 100;
      const nameWidth = width - idWidth;
      const persons = this.state.persons;

      return (
         <Page
            main={
               <div className="PersonaList">
                  <Segment
                     style={{width: width}}
                     color="blue"
                     attached={true}
                  >
                     <span>
                        {persons.length} / {Object.keys(this.props.persons).length} Persons
                     </span>
                     <Input
                        icon="search"
                        placeholder="Filter..."
                        onChange={this.filterChange}
                        style={{position: 'absolute', right: '5px', top: '5px'}}
                     />
                  </Segment>
                  <Table
                     rowHeight={30}
                     rowsCount={persons.length}
                     width={width}
                     height={600}
                     footerHeight={0}
                     headerHeight={30}
                  >
                     <Column
                        header={<Cell>Surname</Cell>}
                        cell={({rowIndex, ...props}: CellProps) => {
                           const p: Person = persons[rowIndex as number];
                           const b = extractYear(p.birthISODate);
                           const d = extractYear(p.deathISODate);
                           return (
                              <Cell {...props} className="name">
                                 <PersonaLink id={p.id} />
                                <span className="lifespan">
                                   <span>{b}</span>
                                   {(b || d) ? ' - ' : ''}
                                   <span>{d}</span>
                                </span>
                              </Cell>
                           );
                        }}
                        isResizable={false}
                        width={nameWidth}
                     />
                     <Column
                        header={<Cell>Id</Cell>}
                        cell={({rowIndex, ...props}: CellProps) => {
                           const p: Person = persons[rowIndex as number];
                           return (
                              <Cell {...props} className="id">
                                 <PersonaLink id={p.id} />
                              </Cell>
                           );
                        }}
                        isResizable={false}
                        width={idWidth}
                     />
                  </Table>
               </div>
            }
         />
      );
   }
}

const PersonaList = connect(
   (state: AppState) => ({
      persons: state.persons,
      allEvents: state.events,
   }),
   (dispatch: GPDispatch) => ({
      dispatch
   }),
)(PersonaListConnected);
export default PersonaList;
